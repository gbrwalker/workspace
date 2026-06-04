import retry from '../utils/retry';

jest.spyOn(console, 'warn').mockImplementation();

describe('retry', () => {
  it('should return result on first success', async () => {
    const fn = jest.fn().mockResolvedValue('ok');
    const result = await retry(fn);
    expect(result).toBe('ok');
    expect(fn).toHaveBeenCalledTimes(1);
  });

  it('should retry on failure and succeed', async () => {
    const fn = jest.fn()
      .mockRejectedValueOnce(new Error('fail1'))
      .mockResolvedValue('ok');

    const result = await retry(fn, { baseDelayMs: 10 });
    expect(result).toBe('ok');
    expect(fn).toHaveBeenCalledTimes(2);
  });

  it('should throw after max retries exceeded', async () => {
    const fn = jest.fn().mockRejectedValue(new Error('always fails'));

    await expect(retry(fn, { maxRetries: 2, baseDelayMs: 10 }))
      .rejects.toThrow('always fails');
    expect(fn).toHaveBeenCalledTimes(2);
  });

  it('should use exponential backoff', async () => {
    const fn = jest.fn()
      .mockRejectedValueOnce(new Error('fail'))
      .mockRejectedValueOnce(new Error('fail'))
      .mockResolvedValue('ok');

    const start = Date.now();
    await retry(fn, { maxRetries: 3, baseDelayMs: 50 });
    const elapsed = Date.now() - start;

    // baseDelay=50: first retry 50ms, second retry 100ms = ~150ms minimum
    expect(elapsed).toBeGreaterThanOrEqual(100);
    expect(fn).toHaveBeenCalledTimes(3);
  });

  it('should respect custom maxRetries', async () => {
    const fn = jest.fn().mockRejectedValue(new Error('nope'));

    await expect(retry(fn, { maxRetries: 1, baseDelayMs: 10 }))
      .rejects.toThrow('nope');
    expect(fn).toHaveBeenCalledTimes(1);
  });
});
