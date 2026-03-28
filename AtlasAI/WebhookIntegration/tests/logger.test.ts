import { logger } from '../src/utils/logger.js';

describe('logger', () => {
  let consoleLogSpy: jest.SpyInstance;
  let consoleErrorSpy: jest.SpyInstance;

  beforeEach(() => {
    consoleLogSpy = jest.spyOn(console, 'log').mockImplementation(() => {});
    consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation(() => {});
  });

  afterEach(() => {
    consoleLogSpy.mockRestore();
    consoleErrorSpy.mockRestore();
  });

  it('info() logs without throwing', () => {
    expect(() => logger.info('info message')).not.toThrow();
    expect(consoleLogSpy).toHaveBeenCalledTimes(1);
  });

  it('warn() logs without throwing', () => {
    expect(() => logger.warn('warn message')).not.toThrow();
    expect(consoleLogSpy).toHaveBeenCalledTimes(1);
  });

  it('error() logs without throwing', () => {
    expect(() => logger.error('error message')).not.toThrow();
    expect(consoleErrorSpy).toHaveBeenCalledTimes(1);
  });

  it('debug() logs without throwing', () => {
    expect(() => logger.debug('debug message')).not.toThrow();
    expect(consoleLogSpy).toHaveBeenCalledTimes(1);
  });

  it('logs with meta object', () => {
    const meta = { key: 'value', count: 42 };
    expect(() => logger.info('message with meta', meta)).not.toThrow();
    const logged = consoleLogSpy.mock.calls[0][0] as string;
    expect(logged).toContain('message with meta');
    expect(logged).toContain('"key"');
    expect(logged).toContain('"value"');
  });
});
