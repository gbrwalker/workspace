import { Page } from 'puppeteer';

import selectors from '../selectors';
import logger from '../utils/logger';
import fillFields from '../apply-form/fillFields';
import waitForNoError from '../apply-form/waitForNoError';
import clickNextButton from '../apply-form/clickNextButton';

async function clickEasyApplyButton(page: Page): Promise<void> {
  await page.waitForSelector(selectors.easyApplyButtonEnabled, { timeout: 10000 });
  await page.click(selectors.easyApplyButtonEnabled);
}

export interface ApplicationFormData {
  phone: string;
  cvPath: string;
  homeCity: string;
  coverLetterPath: string;
  yearsOfExperience: { [key: string]: number };
  languageProficiency: { [key: string]: string };
  requiresVisaSponsorship: boolean;
  booleans: { [key: string]: boolean };
  textFields: { [key: string]: string };
  multipleChoiceFields: { [key: string]: string };
}

interface Params {
  page: Page;
  link: string;
  formData: ApplicationFormData;
  shouldSubmit: boolean;
  maxFormPages?: number;
}

async function apply({ page, link, formData, shouldSubmit, maxFormPages = 10 }: Params): Promise<void> {
  await page.goto(link, { waitUntil: 'load', timeout: 60000 });

  try {
    await clickEasyApplyButton(page);
  } catch {
    logger.warn(`Botão Easy Apply não encontrado: ${link}`);
    return;
  }

  let pagesNavigated = 0;

  while (pagesNavigated < maxFormPages) {
    const submitButton = await page.$(selectors.submit);
    if (submitButton) {
      if (shouldSubmit) {
        await submitButton.click();
        logger.info("Formulário submetido");
      } else {
        logger.info("Modo simulação - formulário NÃO submetido");
      }
      return;
    }

    try {
      await fillFields(page, formData);
    } catch (err) {
      logger.warn(`Erro ao preencher campos na página ${pagesNavigated + 1}`, err);
    }

    try {
      await clickNextButton(page);
    } catch {
      logger.warn(`Botão próximo não encontrado na página ${pagesNavigated + 1}`);
      break;
    }

    try {
      await waitForNoError(page);
    } catch {
      logger.warn(`Erros de validação detectados na página ${pagesNavigated + 1}`);
    }

    pagesNavigated++;
  }

  const finalSubmit = await page.$(selectors.submit);
  if (finalSubmit) {
    if (shouldSubmit) {
      await finalSubmit.click();
      logger.info("Formulário submetido");
    } else {
      logger.info("Modo simulação - formulário NÃO submetido");
    }
  } else {
    throw new Error(`Botão de envio não encontrado após ${pagesNavigated} páginas`);
  }
}

export default apply;
