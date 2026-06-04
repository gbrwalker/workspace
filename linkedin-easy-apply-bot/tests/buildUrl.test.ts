import buildUrl from '../utils/buildUrl';

describe('buildUrl', () => {
  it('should build URL with search params', () => {
    const url = buildUrl('https://www.linkedin.com/jobs/search', {
      keywords: 'javascript',
      location: 'Brazil',
    });

    expect(url.toString()).toBe('https://www.linkedin.com/jobs/search?keywords=javascript&location=Brazil');
  });

  it('should handle special characters in params', () => {
    const url = buildUrl('https://www.linkedin.com/jobs/search', {
      keywords: 'react developer',
      location: 'São Paulo',
    });

    expect(url.searchParams.get('keywords')).toBe('react developer');
    expect(url.searchParams.get('location')).toBe('São Paulo');
  });

  it('should allow updating search params after creation', () => {
    const url = buildUrl('https://www.linkedin.com/jobs/search', {
      start: '0',
    });

    url.searchParams.set('start', '25');
    expect(url.searchParams.get('start')).toBe('25');
  });

  it('should handle empty params', () => {
    const url = buildUrl('https://www.linkedin.com/jobs/search', {});
    expect(url.toString()).toBe('https://www.linkedin.com/jobs/search');
  });
});
