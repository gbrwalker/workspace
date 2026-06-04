import { ElementHandle, Page } from 'puppeteer';

import selectors from '../selectors';
import logger from '../utils/logger';

async function uploadDocs(page: Page, cvPath: string, coverLetterPath: string): Promise<void> {
  const docDivs = await page.$$(selectors.documentUpload);

  for (const docDiv of docDivs) {
    const label = await docDiv.$(selectors.documentUploadLabel) as ElementHandle<HTMLElement>;
    const input = await docDiv.$(selectors.documentUploadInput) as ElementHandle<HTMLInputElement>;

    const text = await label.evaluate((el) => el.innerText.trim().toLowerCase());

    if (text.includes("resume") || text.includes("currículo") || text.includes("curriculo") || text.includes("cv")) {
      if (cvPath) {
        await input.uploadFile(cvPath);
        logger.info(`CV enviado: ${cvPath}`);
      }
    } else if (text.includes("cover") || text.includes("carta") || text.includes("apresentação") || text.includes("apresentacao")) {
      if (coverLetterPath) {
        await input.uploadFile(coverLetterPath);
        logger.info(`Carta de apresentação enviada: ${coverLetterPath}`);
      }
    }
  }
}

export default uploadDocs;
