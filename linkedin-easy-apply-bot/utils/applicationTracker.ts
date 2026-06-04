import fs from 'fs';
import path from 'path';

interface ApplicationRecord {
  link: string;
  title: string;
  companyName: string;
  appliedAt: string;
  status: 'success' | 'error';
  errorMessage?: string;
}

interface TrackerData {
  applications: ApplicationRecord[];
}

const TRACKER_PATH = path.join(__dirname, '..', 'applications.json');

function load(): TrackerData {
  if (!fs.existsSync(TRACKER_PATH)) {
    return { applications: [] };
  }
  const raw = fs.readFileSync(TRACKER_PATH, 'utf-8');
  return JSON.parse(raw);
}

function save(data: TrackerData) {
  fs.writeFileSync(TRACKER_PATH, JSON.stringify(data, null, 2), 'utf-8');
}

function hasApplied(link: string): boolean {
  const jobId = extractJobId(link);
  const data = load();
  return data.applications.some(app => extractJobId(app.link) === jobId && app.status === 'success');
}

function extractJobId(link: string): string {
  const match = link.match(/\/view\/(\d+)/);
  return match ? match[1] : link;
}

function record(entry: Omit<ApplicationRecord, 'appliedAt'>) {
  const data = load();
  data.applications.push({ ...entry, appliedAt: new Date().toISOString() });
  save(data);
}

function getStats(): { total: number; success: number; errors: number } {
  const data = load();
  const success = data.applications.filter(a => a.status === 'success').length;
  return {
    total: data.applications.length,
    success,
    errors: data.applications.length - success,
  };
}

function getSessionStats(sessionStart: string): { total: number; success: number; errors: number; companies: string[] } {
  const data = load();
  const sessionApps = data.applications.filter(a => a.appliedAt >= sessionStart);
  const success = sessionApps.filter(a => a.status === 'success').length;
  const companies = [...new Set(sessionApps.filter(a => a.status === 'success').map(a => a.companyName))];
  return {
    total: sessionApps.length,
    success,
    errors: sessionApps.length - success,
    companies,
  };
}

export default { hasApplied, record, getStats, getSessionStats };
