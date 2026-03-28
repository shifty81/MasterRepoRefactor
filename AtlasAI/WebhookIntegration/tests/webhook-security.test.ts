import crypto from 'crypto';
import { verifyHmacSignature } from '../src/utils/webhook-security.js';

function computeSignature(payload: string, secret: string, prefix = 'sha256='): string {
  return prefix + crypto.createHmac('sha256', secret).update(payload).digest('hex');
}

describe('verifyHmacSignature', () => {
  it('returns true for valid HMAC signature', () => {
    const payload = '{"event":"test"}';
    const secret = 'my-secret';
    const signature = computeSignature(payload, secret);

    expect(verifyHmacSignature(payload, secret, signature)).toBe(true);
  });

  it('returns false for invalid signature', () => {
    const payload = '{"event":"test"}';
    const secret = 'my-secret';
    const wrongSignature = computeSignature(payload, 'wrong-secret');

    expect(verifyHmacSignature(payload, secret, wrongSignature)).toBe(false);
  });

  it('returns true when no secret configured (empty string)', () => {
    expect(verifyHmacSignature('any-payload', '', 'any-signature')).toBe(true);
  });

  it('handles custom prefix', () => {
    const payload = '{"event":"test"}';
    const secret = 'my-secret';
    const customPrefix = 'hmac-';
    const signature = computeSignature(payload, secret, customPrefix);

    expect(verifyHmacSignature(payload, secret, signature, customPrefix)).toBe(true);
  });

  it('returns false when signature length differs', () => {
    const payload = '{"event":"test"}';
    const secret = 'my-secret';
    // Provide a too-short signature so Buffer lengths differ, triggering the catch branch
    expect(verifyHmacSignature(payload, secret, 'sha256=short')).toBe(false);
  });
});
