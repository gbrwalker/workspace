import { ElementHandle, Page } from 'puppeteer';
import LanguageDetect from 'languagedetect';

import buildUrl from '../utils/buildUrl';
import wait from '../utils/wait';
import logger from '../utils/logger';
import retry from '../utils/retry';
import selectors from '../selectors';

const MAX_PAGE_SIZE = 25;
const languageDetector = new LanguageDetect();

async function getJobSearchMetadata({ page, location, keywords }: { page: Page, location: string, keywords: string }) {
  await retry(() => page.goto('https://linkedin.com/jobs', { waitUntil: "load" }));

  await page.type(selectors.keywordInput, keywords);
  await page.waitForSelector(selectors.locationInput, { visible: true });
  await page.$eval(selectors.locationInput, (el, location) => (el as HTMLInputElement).value = location, location);
  await page.type(selectors.locationInput, ' ');
  await page.$eval('button.jobs-search-box__submit-button', (el) => el.click());
  await page.waitForFunction(() => new URLSearchParams(document.location.search).has('geoId'));

  const geoId = await page.evaluate(() => new URLSearchParams(document.location.search).get('geoId'));

  const numJobsHandle = await page.waitForSelector(selectors.searchResultListText, { timeout: 10000 }) as ElementHandle<HTMLElement>;
  const numAvailableJobs = await numJobsHandle.evaluate((el) => parseInt((el as HTMLElement).innerText.replace(/[,.\s]/g, '')));

  return {
    geoId,
    numAvailableJobs
  };
}

interface PARAMS {
  page: Page,
  location: string,
  keywords: string,
  workplace: { remote: boolean, onSite: boolean, hybrid: boolean },
  jobTitle: string,
  jobDescription: string,
  jobDescriptionLanguages: string[],
  blacklistCompanies?: string[],
}

async function* fetchJobLinksUser({ page, location, keywords, workplace: { remote, onSite, hybrid }, jobTitle, jobDescription, jobDescriptionLanguages, blacklistCompanies = [] }: PARAMS): AsyncGenerator<[string, string, string]> {
  let numSeenJobs = 0;
  let numMatchingJobs = 0;
  let numBlacklisted = 0;
  const fWt = [onSite, remote, hybrid].reduce((acc, c, i) => c ? [...acc, i + 1] : acc, [] as number[]).join(',');

  const { geoId, numAvailableJobs } = await getJobSearchMetadata({ page, location, keywords });
  logger.info(`Total de vagas disponíveis: ${numAvailableJobs}`);

  const searchParams: { [key: string]: string } = {
    keywords,
    location,
    start: numSeenJobs.toString(),
    f_WT: fWt,
    f_AL: 'true'
  };

  if (geoId) {
    searchParams.geoId = geoId.toString();
  }

  const url = buildUrl('https://www.linkedin.com/jobs/search', searchParams);

  const jobTitleRegExp = new RegExp(jobTitle, 'i');
  const jobDescriptionRegExp = new RegExp(jobDescription, 'i');
  const blacklistRegExps = blacklistCompanies.map(c => new RegExp(c, 'i'));

  while (numSeenJobs < numAvailableJobs) {
    url.searchParams.set('start', numSeenJobs.toString());

    try {
      await retry(() => page.goto(url.toString(), { waitUntil: "load" }));
    } catch (err) {
      logger.error(`Falha ao carregar página de resultados (start=${numSeenJobs})`, err);
      break;
    }

    const expectedItems = Math.min(MAX_PAGE_SIZE, numAvailableJobs - numSeenJobs);
    await page.waitForSelector(`${selectors.searchResultListItem}:nth-child(${expectedItems})`, { timeout: 10000 }).catch(() => {
      logger.warn(`Timeout esperando ${expectedItems} resultados, continuando com o que tem`);
    });

    const jobListings = await page.$$(selectors.searchResultListItem);

    for (let i = 0; i < jobListings.length; i++) {
      try {
        const [link, title] = await page.$eval(`${selectors.searchResultListItem}:nth-child(${i + 1}) ${selectors.searchResultListItemLink}`, (el) => {
          const linkEl = el as HTMLLinkElement;
          linkEl.click();
          return [linkEl.href.trim(), linkEl.innerText.trim()];
        });

        await page.waitForFunction(async (selectors) => {
          const hasLoadedDescription = !!document.querySelector<HTMLElement>(selectors.jobDescription)?.innerText.trim();
          const hasLoadedStatus = !!(document.querySelector(selectors.easyApplyButtonEnabled) || document.querySelector(selectors.appliedToJobFeedback));
          return hasLoadedStatus && hasLoadedDescription;
        }, { timeout: 10000 }, selectors);

        const companyName = await page.$eval(`${selectors.searchResultListItem}:nth-child(${i + 1}) ${selectors.searchResultListItemCompanyName}`, el => (el as HTMLElement).innerText).catch(() => 'Desconhecida');

        if (blacklistRegExps.some(re => re.test(companyName))) {
          numBlacklisted++;
          logger.info(`Empresa na blacklist: ${companyName} - pulando`);
          continue;
        }

        const jobDescriptionText = await page.$eval(selectors.jobDescription, el => (el as HTMLElement).innerText);
        const canApply = !!(await page.$(selectors.easyApplyButtonEnabled));

        let matchesLanguage = jobDescriptionLanguages.includes("any");
        if (!matchesLanguage) {
          const detected = languageDetector.detect(jobDescriptionText, 3);
          matchesLanguage = detected.some(([lang]) => jobDescriptionLanguages.includes(lang));
        }

        if (canApply && jobTitleRegExp.test(title) && jobDescriptionRegExp.test(jobDescriptionText) && matchesLanguage) {
          numMatchingJobs++;
          logger.info(`[${numMatchingJobs}] Match: ${title} @ ${companyName}`);
          yield [link, title, companyName];
        }
      } catch (e) {
        logger.warn(`Erro ao processar vaga ${i + 1} na página`, e);
      }
    }

    await wait(2000);
    numSeenJobs += jobListings.length;
    logger.info(`Progresso: ${numSeenJobs}/${numAvailableJobs} vagas analisadas | ${numMatchingJobs} matches | ${numBlacklisted} blacklisted`);
  }
}

export default fetchJobLinksUser;
