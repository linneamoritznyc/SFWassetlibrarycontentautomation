import { describe, expect, it } from 'vitest';
import { originalWords } from './scout_rank.js';

const item = { title: 'Solo vivo em Minas Gerais', summary: 'Um estudo da Embrapa.' };

describe('keeping the source language on a Scout card', () => {
  it('keeps nothing extra for an English item', () => {
    expect(originalWords({ language: 'en', original_title: '' }, item)).toEqual({
      originalTitle: null,
      originalSummary: null,
    });
  });

  it('treats regional English as English', () => {
    for (const language of ['en-GB', 'en-IN', 'EN', ' en ']) {
      expect(originalWords({ language, original_title: 'x' }, item).originalTitle).toBeNull();
    }
  });

  it('keeps the source words for anything else', () => {
    expect(originalWords({ language: 'pt-BR', original_title: 'Solo vivo' }, item)).toEqual({
      originalTitle: 'Solo vivo',
      originalSummary: 'Um estudo da Embrapa.',
    });
  });

  it('falls back to the feed title when the model returns none', () => {
    expect(originalWords({ language: 'ta', original_title: '   ' }, item).originalTitle).toBe(
      'Solo vivo em Minas Gerais',
    );
  });

  it('is not fooled by a language tag that merely starts with the letters en', () => {
    // "enm" is Middle English and "eng" is the three-letter code, but a tag
    // like "en_GB" with an underscore is the shape that a naive startsWith
    // would wave through while a hypothetical "enz" is not English at all.
    expect(originalWords({ language: 'enz', original_title: 'x' }, item).originalTitle).toBe('x');
  });

  it('stores null rather than an empty string when there is nothing to keep', () => {
    expect(
      originalWords({ language: 'fr', original_title: '' }, { title: null, summary: null }),
    ).toEqual({ originalTitle: null, originalSummary: null });
  });
});
