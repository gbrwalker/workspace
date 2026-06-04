import puppeteer, { Page } from "puppeteer";
import config from "../config";

import ask from "../utils/ask";
import logger from "../utils/logger";
import tracker from "../utils/applicationTracker";
import login from "../login";
import apply, { ApplicationFormData } from "../apply";
import fetchJobLinksUser from "../fetch/fetchJobLinksUser";

interface AppState {
  paused: boolean;
}

const wait = (time: number) => new Promise((resolve) => setTimeout(resolve, time));

const state: AppState = {
  paused: false,
};

const askForPauseInput = async () => {
  await ask("press enter to pause the program");

  state.paused = true;

  await ask("finishing job application...\n");

  state.paused = false;
  logger.info("Unpaused");

  askForPauseInput();
};

function selectCvForJob(title: string): string {
  if (config.CV_MAPPING && config.CV_MAPPING.length > 0) {
    for (const mapping of config.CV_MAPPING) {
      if (new RegExp(mapping.jobTitleRegex, 'i').test(title)) {
        logger.info(`CV selecionado por mapeamento: ${mapping.cvPath}`);
        return mapping.cvPath;
      }
    }
  }
  return config.CV_PATH;
}

(async () => {
  const sessionStart = new Date().toISOString();
  const shouldSubmit = process.argv[2] === "SUBMIT";
  let jobsFound = 0;
  let jobsSkippedDuplicate = 0;

  logger.info("=== LinkedIn Easy Apply Bot - Iniciando ===");
  logger.info(`Modo: ${shouldSubmit ? "APLICANDO (SUBMIT)" : "SIMULAÇÃO (dry-run)"}`);
  logger.info(`Keywords: ${config.KEYWORDS} | Local: ${config.LOCATION}`);

  const browser = await puppeteer.launch({
    headless: config.HEADLESS ?? false,
    ignoreHTTPSErrors: true,
    args: ["--disable-setuid-sandbox", "--no-sandbox"],
  });
  const context = await browser.createIncognitoBrowserContext();
  const listingPage = await context.newPage();

  const pages = await browser.pages();
  await pages[0].close();

  await login({
    page: listingPage,
    email: config.LINKEDIN_EMAIL,
    password: config.LINKEDIN_PASSWORD,
  });

  askForPauseInput();

  const linkGenerator = fetchJobLinksUser({
    page: listingPage,
    location: config.LOCATION,
    keywords: config.KEYWORDS,
    workplace: {
      remote: config.WORKPLACE.REMOTE,
      onSite: config.WORKPLACE.ON_SITE,
      hybrid: config.WORKPLACE.HYBRID,
    },
    jobTitle: config.JOB_TITLE,
    jobDescription: config.JOB_DESCRIPTION,
    jobDescriptionLanguages: config.JOB_DESCRIPTION_LANGUAGES,
    blacklistCompanies: config.BLACKLIST_COMPANIES ?? [],
  });

  let applicationPage: Page | null = null;

  for await (const [link, title, companyName] of linkGenerator) {
    jobsFound++;

    if (tracker.hasApplied(link)) {
      jobsSkippedDuplicate++;
      logger.info(`Já aplicado anteriormente: ${title} @ ${companyName} - pulando`);
      continue;
    }

    if (!applicationPage || !config.SINGLE_PAGE) {
      applicationPage = await context.newPage();
    }

    await applicationPage.bringToFront();

    const cvPath = selectCvForJob(title);

    try {
      const formData: ApplicationFormData = {
        phone: config.PHONE,
        cvPath,
        homeCity: config.HOME_CITY,
        coverLetterPath: config.COVER_LETTER_PATH,
        yearsOfExperience: config.YEARS_OF_EXPERIENCE,
        languageProficiency: config.LANGUAGE_PROFICIENCY,
        requiresVisaSponsorship: config.REQUIRES_VISA_SPONSORSHIP,
        booleans: config.BOOLEANS,
        textFields: config.TEXT_FIELDS,
        multipleChoiceFields: config.MULTIPLE_CHOICE_FIELDS,
      };

      await apply({
        page: applicationPage,
        link,
        formData,
        shouldSubmit,
        maxFormPages: config.MAX_FORM_PAGES ?? 10,
      });

      tracker.record({ link, title, companyName, status: 'success' });
      logger.success(`Aplicado: ${title} @ ${companyName}`);
    } catch (err) {
      tracker.record({ link, title, companyName, status: 'error', errorMessage: String(err) });
      logger.error(`Falha ao aplicar: ${title} @ ${companyName}`, err);
    }

    await listingPage.bringToFront();

    for (let shouldLog = true; state.paused; shouldLog = false) {
      shouldLog && logger.info("Programa pausado, pressione enter para continuar");
      await wait(2000);
    }
  }

  // Relatório final
  const stats = tracker.getSessionStats(sessionStart);
  logger.info("=== RELATÓRIO DA SESSÃO ===");
  logger.info(`Vagas encontradas (match): ${jobsFound}`);
  logger.info(`Vagas puladas (já aplicadas): ${jobsSkippedDuplicate}`);
  logger.info(`Candidaturas enviadas: ${stats.success}`);
  logger.info(`Candidaturas com erro: ${stats.errors}`);
  if (stats.companies.length > 0) {
    logger.info(`Empresas: ${stats.companies.join(', ')}`);
  }
  const allTimeStats = tracker.getStats();
  logger.info(`Total histórico de candidaturas: ${allTimeStats.total} (${allTimeStats.success} ok, ${allTimeStats.errors} erros)`);
  logger.info("===========================");

  await browser.close();
})();
