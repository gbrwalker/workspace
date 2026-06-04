import fs from 'fs';
import path from 'path';

type LogLevel = 'INFO' | 'WARN' | 'ERROR' | 'SUCCESS';

const LOG_DIR = path.join(__dirname, '..', 'logs');
const timestamp = () => new Date().toISOString();

let logFilePath: string;

function ensureLogDir() {
  if (!fs.existsSync(LOG_DIR)) {
    fs.mkdirSync(LOG_DIR, { recursive: true });
  }
  if (!logFilePath) {
    const dateStr = new Date().toISOString().replace(/[:.]/g, '-');
    logFilePath = path.join(LOG_DIR, `run-${dateStr}.log`);
  }
}

function formatMessage(level: LogLevel, message: string): string {
  return `[${timestamp()}] [${level}] ${message}`;
}

function writeToFile(formatted: string) {
  ensureLogDir();
  fs.appendFileSync(logFilePath, formatted + '\n');
}

function info(message: string) {
  const formatted = formatMessage('INFO', message);
  console.log(formatted);
  writeToFile(formatted);
}

function warn(message: string, err?: unknown) {
  const errMsg = err instanceof Error ? err.message : (err ? String(err) : '');
  const formatted = formatMessage('WARN', errMsg ? `${message}: ${errMsg}` : message);
  console.warn(formatted);
  writeToFile(formatted);
}

function error(message: string, err?: unknown) {
  const errMsg = err instanceof Error ? err.message : String(err ?? '');
  const formatted = formatMessage('ERROR', errMsg ? `${message}: ${errMsg}` : message);
  console.error(formatted);
  writeToFile(formatted);
}

function success(message: string) {
  const formatted = formatMessage('SUCCESS', message);
  console.log(formatted);
  writeToFile(formatted);
}

export default { info, warn, error, success };
