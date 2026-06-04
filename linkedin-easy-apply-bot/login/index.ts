import { Page } from 'puppeteer';

import ask from '../utils/ask';
import logger from '../utils/logger';
import retry from '../utils/retry';
import selectors from '../selectors';

interface Params {
  page: Page;
  email: string;
  password: string;
}

async function login({ page, email, password }: Params): Promise<void> {
  await retry(() => page.goto('https://www.linkedin.com/login', { waitUntil: 'load' }));

  await page.type(selectors.emailInput, email);
  await page.type(selectors.passwordInput, password);

  await page.click(selectors.loginSubmit);
  await page.waitForNavigation({ waitUntil: 'load' });

  const captcha = await page.$(selectors.captcha);

  if (captcha) {
    await ask('Resolva o CAPTCHA no navegador e pressione enter aqui');
    await page.goto('https://www.linkedin.com/', { waitUntil: 'load' });
  }

  logger.success('Login realizado no LinkedIn');

  await page.click(selectors.skipButton).catch(() => {});
}

export default login;
