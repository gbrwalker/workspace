import { Page } from 'puppeteer';

import fillMultipleChoiceFields from './fillMultipleChoiceFields';
import fillBoolean from './fillBoolean';
import fillTextFields from './fillTextFields';
import insertHomeCity from './insertHomeCity';
import insertPhone from './insertPhone';
import uncheckFollowCompany from './uncheckFollowCompany';
import uploadDocs from './uploadDocs';
import logger from '../utils/logger';
import { ApplicationFormData } from '../apply';

async function fillFields(page: Page, formData: ApplicationFormData): Promise<void> {
  await insertHomeCity(page, formData.homeCity).catch(err =>
    logger.warn('Campo cidade não encontrado ou erro ao preencher', err)
  );

  await insertPhone(page, formData.phone).catch(err =>
    logger.warn('Campo telefone não encontrado ou erro ao preencher', err)
  );

  await uncheckFollowCompany(page);

  await uploadDocs(page, formData.cvPath, formData.coverLetterPath).catch(err =>
    logger.warn('Erro no upload de documentos', err)
  );

  const textFields = {
    ...formData.textFields,
    ...formData.yearsOfExperience,
  };

  await fillTextFields(page, textFields).catch(err =>
    logger.warn('Erro ao preencher campos de texto', err)
  );

  const booleans = { ...formData.booleans };
  booleans['sponsorship'] = formData.requiresVisaSponsorship;

  await fillBoolean(page, booleans).catch(err =>
    logger.warn('Erro ao preencher campos booleanos', err)
  );

  const multipleChoiceFields = {
    ...formData.languageProficiency,
    ...formData.multipleChoiceFields,
  };

  await fillMultipleChoiceFields(page, multipleChoiceFields).catch(err =>
    logger.warn('Erro ao preencher campos de múltipla escolha', err)
  );
}

export default fillFields;
