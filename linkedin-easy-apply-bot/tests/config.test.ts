import sampleConfig from '../sample_config';

describe('sample_config', () => {
  it('should have all required login fields', () => {
    expect(sampleConfig).toHaveProperty('LINKEDIN_EMAIL');
    expect(sampleConfig).toHaveProperty('LINKEDIN_PASSWORD');
  });

  it('should have all required search parameters', () => {
    expect(sampleConfig).toHaveProperty('KEYWORDS');
    expect(sampleConfig).toHaveProperty('LOCATION');
    expect(sampleConfig).toHaveProperty('WORKPLACE');
    expect(sampleConfig.WORKPLACE).toHaveProperty('REMOTE');
    expect(sampleConfig.WORKPLACE).toHaveProperty('ON_SITE');
    expect(sampleConfig.WORKPLACE).toHaveProperty('HYBRID');
    expect(sampleConfig).toHaveProperty('JOB_TITLE');
    expect(sampleConfig).toHaveProperty('JOB_DESCRIPTION');
    expect(sampleConfig).toHaveProperty('JOB_DESCRIPTION_LANGUAGES');
  });

  it('should have all form data fields', () => {
    expect(sampleConfig).toHaveProperty('PHONE');
    expect(sampleConfig).toHaveProperty('CV_PATH');
    expect(sampleConfig).toHaveProperty('COVER_LETTER_PATH');
    expect(sampleConfig).toHaveProperty('HOME_CITY');
    expect(sampleConfig).toHaveProperty('YEARS_OF_EXPERIENCE');
    expect(sampleConfig).toHaveProperty('LANGUAGE_PROFICIENCY');
    expect(sampleConfig).toHaveProperty('REQUIRES_VISA_SPONSORSHIP');
    expect(sampleConfig).toHaveProperty('TEXT_FIELDS');
    expect(sampleConfig).toHaveProperty('BOOLEANS');
    expect(sampleConfig).toHaveProperty('MULTIPLE_CHOICE_FIELDS');
  });

  it('should have new feature fields', () => {
    expect(sampleConfig).toHaveProperty('BLACKLIST_COMPANIES');
    expect(Array.isArray(sampleConfig.BLACKLIST_COMPANIES)).toBe(true);
    expect(sampleConfig).toHaveProperty('CV_MAPPING');
    expect(Array.isArray(sampleConfig.CV_MAPPING)).toBe(true);
    expect(sampleConfig).toHaveProperty('HEADLESS');
    expect(typeof sampleConfig.HEADLESS).toBe('boolean');
    expect(sampleConfig).toHaveProperty('MAX_FORM_PAGES');
    expect(typeof sampleConfig.MAX_FORM_PAGES).toBe('number');
    expect(sampleConfig).toHaveProperty('SINGLE_PAGE');
    expect(typeof sampleConfig.SINGLE_PAGE).toBe('boolean');
  });

  it('should have valid JOB_TITLE regex', () => {
    const regex = new RegExp(sampleConfig.JOB_TITLE, 'i');
    expect(regex.test('Frontend Developer')).toBe(true);
    expect(regex.test('React Engineer')).toBe(true);
    expect(regex.test('Node.js Developer')).toBe(true);
    expect(regex.test('Desenvolvedor TypeScript')).toBe(true);
    expect(regex.test('Marketing Manager')).toBe(false);
  });

  it('should have valid BOOLEANS regex keys', () => {
    const keys = Object.keys(sampleConfig.BOOLEANS);
    for (const key of keys) {
      expect(() => new RegExp(key, 'i')).not.toThrow();
    }
  });

  it('should have JOB_DESCRIPTION_LANGUAGES as array', () => {
    expect(Array.isArray(sampleConfig.JOB_DESCRIPTION_LANGUAGES)).toBe(true);
    expect(sampleConfig.JOB_DESCRIPTION_LANGUAGES.length).toBeGreaterThan(0);
  });
});
