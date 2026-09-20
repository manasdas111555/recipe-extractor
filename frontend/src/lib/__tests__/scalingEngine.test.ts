import { describe, it, expect } from 'vitest';
import { scaleIngredientItem, parseQuantity, formatQuantity } from '../../utils/scalingEngine';

describe('ScalingEngine - Hinglish Culinary Metric Scaling (Rule 13)', () => {
  it('handles "1 bowl (~150 ml, approx)" scaling quantity 2x while scaling parenthetical volume note', () => {
    const rawIngredient = '1 bowl (~150 ml, approx) paneer';
    const scaled = scaleIngredientItem(rawIngredient, 0, 2, 4); // 2x scaling (2 -> 4 servings)

    expect(scaled.quantity).toBe(2);
    expect(scaled.displayQuantity).toBe('2');
    expect(scaled.unit).toBe('bowl');
    expect(scaled.parentheticalNote).toContain('300ml');
    expect(scaled.parentheticalNote).toContain('approx');
    expect(scaled.scaledText).toContain('2 bowl paneer');
  });

  it('handles "2 tbsp (approx) ghee" scaling quantity 1.5x (from 2 to 3 servings)', () => {
    const rawIngredient = '2 tbsp (approx) ghee';
    const scaled = scaleIngredientItem(rawIngredient, 0, 2, 3); // 1.5x scaling

    expect(scaled.quantity).toBe(3);
    expect(scaled.displayQuantity).toBe('3');
    expect(scaled.unit).toBe('tbsp');
    expect(scaled.scaledText).toContain('3 tbsp ghee');
  });
});
