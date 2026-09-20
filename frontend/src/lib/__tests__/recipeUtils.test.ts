import { describe, it, expect } from 'vitest';
import {
  resolveMediaPreview,
  cleanLineLeadingNumerics,
  formatCleanTitle,
  parseIngredients,
  formatTurnaroundTime,
  parseRecipeSections,
  generateStructuredText,
} from '../recipeUtils';

describe('recipeUtils - Pure Frontend Utilities', () => {
  describe('cleanLineLeadingNumerics', () => {
    it('keeps normal words intact ("Salt" -> "Salt")', () => {
      expect(cleanLineLeadingNumerics('Salt')).toBe('Salt');
      expect(cleanLineLeadingNumerics('  Salt  ')).toBe('Salt');
    });

    it('strips leading numbers and dots ("1. Salt" -> "Salt")', () => {
      expect(cleanLineLeadingNumerics('1. Salt')).toBe('Salt');
      expect(cleanLineLeadingNumerics('12.   Black Pepper')).toBe('Black Pepper');
      expect(cleanLineLeadingNumerics('3) Cumin Seeds')).toBe('Cumin Seeds');
      expect(cleanLineLeadingNumerics('4 - Turmeric')).toBe('Turmeric');
    });
  });

  describe('formatCleanTitle', () => {
    it('removes markdown headings and bold markers', () => {
      expect(formatCleanTitle('## Spicy Paneer Butter Masala')).toBe('Spicy Paneer Butter Masala');
      expect(formatCleanTitle('**Paneer Butter Masala**')).toBe('Paneer Butter Masala');
    });
  });

  describe('parseIngredients', () => {
    it('keeps "all-purpose flour" intact without splitting on space', () => {
      const parsed = parseIngredients('1. all-purpose flour');
      expect(parsed).toEqual([{ name: 'all-purpose flour' }]);
    });

    it('splits on explicit delimiters like "-" or ":" or "(" for quantity', () => {
      const parsed = parseIngredients('Paneer - 200g\nButter : 2 tbsp\nSalt (1 tsp)');
      expect(parsed[0]).toEqual({ name: 'Paneer', quantity: '200g' });
      expect(parsed[1]).toEqual({ name: 'Butter', quantity: '2 tbsp' });
      expect(parsed[2]).toEqual({ name: 'Salt', quantity: '1 tsp' });
    });
  });

  describe('formatTurnaroundTime', () => {
    it('formats millisecond deltas into seconds', () => {
      expect(formatTurnaroundTime(2500)).toBe('2.5s');
      expect(formatTurnaroundTime(800)).toBe('0.8s');
      expect(formatTurnaroundTime(0)).toBe('0.0s');
    });
  });

  describe('resolveMediaPreview', () => {
    it('resolves Instagram Reels preview with stream tokens', () => {
      const result = {
        source_url: 'https://www.instagram.com/reel/C9876543210/',
        stream_token: 'signed_test_token_123',
        job_id: 'job_456'
      };
      const preview = resolveMediaPreview(result);
      expect(preview?.type).toBe('instagram');
      expect(preview?.id).toBe('C9876543210');
      expect(preview?.streamSrc).toContain('/api/v1/extract/stream-video?token=signed_test_token_123');
    });

    it('resolves YouTube Shorts iframe preview', () => {
      const result = {
        source_url: 'https://www.youtube.com/shorts/KrFDs2M_FSE'
      };
      const preview = resolveMediaPreview(result);
      expect(preview?.type).toBe('youtube');
      expect(preview?.id).toBe('KrFDs2M_FSE');
      expect(preview?.src).toContain('youtube-nocookie.com/embed/KrFDs2M_FSE');
    });
  });

  describe('generateStructuredText', () => {
    it('generates structured text payload without errors', () => {
      const meta = {
        title: 'Paneer Tikka',
        category: 'RECIPE',
        summary: 'Delicious grilled paneer tikka.',
        ingredients: [{ name: 'Paneer', quantity: '200g' }],
        instructions: ['Cut paneer into cubes', 'Grill for 10 mins']
      };
      const text = generateStructuredText(meta, false);
      expect(text).toContain('Paneer Tikka');
      expect(text).toContain('Paneer - 200g');
      expect(text).toContain('Cut paneer into cubes');
    });
  });
});
