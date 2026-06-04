export default {
  // LOGIN DETAILS (use env vars: LINKEDIN_EMAIL and LINKEDIN_PASSWORD)
  LINKEDIN_EMAIL: process.env.LINKEDIN_EMAIL || "",
  LINKEDIN_PASSWORD: process.env.LINKEDIN_PASSWORD || "",

  // JOB SEARCH PARAMETERS
  KEYWORDS: "javascript",
  LOCATION: "Brazil",
  WORKPLACE: {
    REMOTE: true,
    ON_SITE: false,
    HYBRID: true,
  },
  JOB_TITLE: "(javascript|frontend|front-end|fullstack|full-stack|nodejs|node|react|typescript).*(developer|engineer|desenvolvedor|engenheiro)|(desenvolvedor|engenheiro).*(javascript|frontend|front-end|fullstack|full-stack|nodejs|node|react|typescript)",
  JOB_DESCRIPTION: "^((?!(empresa_bloqueada))(.|[\n\r]))*$",
  JOB_DESCRIPTION_LANGUAGES: ["portuguese", "english"],

  // COMPANY BLACKLIST - skip jobs from these companies (case-insensitive)
  BLACKLIST_COMPANIES: [] as string[],

  // FORM DATA
  PHONE: "",
  CV_PATH: "",
  COVER_LETTER_PATH: "",
  HOME_CITY: "",
  YEARS_OF_EXPERIENCE: {
    "angular": 0,
    "react": 0,
    "node": 0,
    "javascript": 0,
    "typescript": 0,
    "python": 0,
    "html": 0,
    "css": 0,
    "docker": 0,
    "git": 0,
  } as { [key: string]: number },
  LANGUAGE_PROFICIENCY: {
    "english": "professional",
    "portuguese": "native",
  } as { [key: string]: string },
  REQUIRES_VISA_SPONSORSHIP: false,
  TEXT_FIELDS: {} as { [key: string]: string },
  BOOLEANS: {
    "bachelor|bacharelado|graduação": true,
    "authorized|autorizado": true,
  } as { [key: string]: boolean },
  MULTIPLE_CHOICE_FIELDS: {} as { [key: string]: string },

  // CV MAPPING - select CV based on job title regex (first match wins, falls back to CV_PATH)
  CV_MAPPING: [] as { jobTitleRegex: string; cvPath: string }[],

  // SETTINGS
  SINGLE_PAGE: true,
  HEADLESS: false,
  MAX_FORM_PAGES: 10,
}
