import fs from 'fs';
import path from 'path';
import logger from '../utils/logger';

const LOG_DIR = path.join(__dirname, '..', 'logs');

afterAll(() => {
  if (fs.existsSync(LOG_DIR)) {
    const files = fs.readdirSync(LOG_DIR);
    for (const file of files) {
      fs.unlinkSync(path.join(LOG_DIR, file));
    }
    fs.rmdirSync(LOG_DIR);
  }
});

describe('logger', () => {
  it('should log info messages to console and file', () => {
    const spy = jest.spyOn(console, 'log').mockImplementation();
    logger.info('test info message');
    expect(spy).toHaveBeenCalledWith(expect.stringContaining('[INFO] test info message'));
    spy.mockRestore();
  });

  it('should log warn messages', () => {
    const spy = jest.spyOn(console, 'warn').mockImplementation();
    logger.warn('test warn');
    expect(spy).toHaveBeenCalledWith(expect.stringContaining('[WARN] test warn'));
    spy.mockRestore();
  });

  it('should log warn with error context', () => {
    const spy = jest.spyOn(console, 'warn').mockImplementation();
    logger.warn('something failed', new Error('oops'));
    expect(spy).toHaveBeenCalledWith(expect.stringContaining('something failed: oops'));
    spy.mockRestore();
  });

  it('should log error messages with Error objects', () => {
    const spy = jest.spyOn(console, 'error').mockImplementation();
    logger.error('crash', new Error('boom'));
    expect(spy).toHaveBeenCalledWith(expect.stringContaining('[ERROR] crash: boom'));
    spy.mockRestore();
  });

  it('should log error messages with string errors', () => {
    const spy = jest.spyOn(console, 'error').mockImplementation();
    logger.error('crash', 'string error');
    expect(spy).toHaveBeenCalledWith(expect.stringContaining('[ERROR] crash: string error'));
    spy.mockRestore();
  });

  it('should log success messages', () => {
    const spy = jest.spyOn(console, 'log').mockImplementation();
    logger.success('done');
    expect(spy).toHaveBeenCalledWith(expect.stringContaining('[SUCCESS] done'));
    spy.mockRestore();
  });

  it('should create log directory and write to file', () => {
    expect(fs.existsSync(LOG_DIR)).toBe(true);
    const files = fs.readdirSync(LOG_DIR).filter(f => f.endsWith('.log'));
    expect(files.length).toBeGreaterThan(0);

    const allContent = files.map(f => fs.readFileSync(path.join(LOG_DIR, f), 'utf-8')).join('\n');
    expect(allContent).toContain('[INFO]');
    expect(allContent).toContain('[WARN]');
    expect(allContent).toContain('[ERROR]');
    expect(allContent).toContain('[SUCCESS]');
  });
});
