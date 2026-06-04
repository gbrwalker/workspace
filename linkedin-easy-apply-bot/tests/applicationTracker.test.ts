import fs from 'fs';
import path from 'path';
import tracker from '../utils/applicationTracker';

const TRACKER_PATH = path.join(__dirname, '..', 'applications.json');

beforeEach(() => {
  if (fs.existsSync(TRACKER_PATH)) {
    fs.unlinkSync(TRACKER_PATH);
  }
});

afterAll(() => {
  if (fs.existsSync(TRACKER_PATH)) {
    fs.unlinkSync(TRACKER_PATH);
  }
});

describe('applicationTracker', () => {
  it('should return false for hasApplied when no data exists', () => {
    expect(tracker.hasApplied('https://linkedin.com/jobs/view/12345')).toBe(false);
  });

  it('should record a successful application', () => {
    tracker.record({
      link: 'https://linkedin.com/jobs/view/12345',
      title: 'Frontend Dev',
      companyName: 'Acme',
      status: 'success',
    });

    expect(tracker.hasApplied('https://linkedin.com/jobs/view/12345')).toBe(true);
  });

  it('should not mark as applied if status is error', () => {
    tracker.record({
      link: 'https://linkedin.com/jobs/view/99999',
      title: 'Backend Dev',
      companyName: 'Corp',
      status: 'error',
      errorMessage: 'Submit button not found',
    });

    expect(tracker.hasApplied('https://linkedin.com/jobs/view/99999')).toBe(false);
  });

  it('should detect duplicates by job ID in URL', () => {
    tracker.record({
      link: 'https://linkedin.com/jobs/view/55555/?refId=abc',
      title: 'Dev',
      companyName: 'X',
      status: 'success',
    });

    expect(tracker.hasApplied('https://linkedin.com/jobs/view/55555/?refId=xyz')).toBe(true);
  });

  it('should track multiple applications', () => {
    tracker.record({ link: 'https://linkedin.com/jobs/view/111', title: 'A', companyName: 'X', status: 'success' });
    tracker.record({ link: 'https://linkedin.com/jobs/view/222', title: 'B', companyName: 'Y', status: 'success' });
    tracker.record({ link: 'https://linkedin.com/jobs/view/333', title: 'C', companyName: 'Z', status: 'error' });

    const stats = tracker.getStats();
    expect(stats.total).toBe(3);
    expect(stats.success).toBe(2);
    expect(stats.errors).toBe(1);
  });

  it('should return session-scoped stats', () => {
    const beforeSession = new Date().toISOString();

    tracker.record({ link: 'https://linkedin.com/jobs/view/1', title: 'J1', companyName: 'C1', status: 'success' });
    tracker.record({ link: 'https://linkedin.com/jobs/view/2', title: 'J2', companyName: 'C2', status: 'success' });
    tracker.record({ link: 'https://linkedin.com/jobs/view/3', title: 'J3', companyName: 'C1', status: 'error' });

    const sessionStats = tracker.getSessionStats(beforeSession);
    expect(sessionStats.total).toBe(3);
    expect(sessionStats.success).toBe(2);
    expect(sessionStats.errors).toBe(1);
    expect(sessionStats.companies).toContain('C1');
    expect(sessionStats.companies).toContain('C2');
  });

  it('should persist data to disk', () => {
    tracker.record({ link: 'https://linkedin.com/jobs/view/777', title: 'Persist', companyName: 'Disk', status: 'success' });

    expect(fs.existsSync(TRACKER_PATH)).toBe(true);
    const raw = JSON.parse(fs.readFileSync(TRACKER_PATH, 'utf-8'));
    expect(raw.applications).toHaveLength(1);
    expect(raw.applications[0].title).toBe('Persist');
    expect(raw.applications[0].appliedAt).toBeDefined();
  });
});
