import fs from 'fs';
import path from 'path';

const TRACKER_PATH = path.join(__dirname, '..', 'applications.json');

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

function run() {
  if (!fs.existsSync(TRACKER_PATH)) {
    console.log('Nenhuma candidatura registrada ainda.');
    return;
  }

  const data: TrackerData = JSON.parse(fs.readFileSync(TRACKER_PATH, 'utf-8'));
  const apps = data.applications;
  const successful = apps.filter(a => a.status === 'success');
  const failed = apps.filter(a => a.status === 'error');
  const companies = [...new Set(successful.map(a => a.companyName))];

  console.log('=== ESTATÍSTICAS DO BOT ===');
  console.log(`Total de candidaturas: ${apps.length}`);
  console.log(`  Sucesso: ${successful.length}`);
  console.log(`  Erros: ${failed.length}`);
  console.log(`Empresas únicas: ${companies.length}`);
  console.log('');

  if (successful.length > 0) {
    const first = successful[0];
    const last = successful[successful.length - 1];
    console.log(`Primeira candidatura: ${new Date(first.appliedAt).toLocaleString('pt-BR')}`);
    console.log(`Última candidatura: ${new Date(last.appliedAt).toLocaleString('pt-BR')}`);
    console.log('');

    const byCompany: { [key: string]: number } = {};
    for (const app of successful) {
      byCompany[app.companyName] = (byCompany[app.companyName] || 0) + 1;
    }

    console.log('--- Candidaturas por empresa ---');
    const sorted = Object.entries(byCompany).sort((a, b) => b[1] - a[1]);
    for (const [company, count] of sorted) {
      console.log(`  ${company}: ${count}`);
    }
  }

  if (failed.length > 0) {
    console.log('');
    console.log('--- Últimos erros ---');
    const lastErrors = failed.slice(-5);
    for (const err of lastErrors) {
      console.log(`  ${err.title} @ ${err.companyName}: ${err.errorMessage?.substring(0, 80)}`);
    }
  }

  console.log('===========================');
}

run();
