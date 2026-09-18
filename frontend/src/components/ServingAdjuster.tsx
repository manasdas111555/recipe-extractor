'use client';

import React, { useState } from 'react';
import { Users, Minus, Plus, ShoppingCart, Copy, Check } from 'lucide-react';

interface Ingredient {
  name: string;
  quantity?: string | number;
  unit?: string;
  notes?: string;
}

import { scaleIngredientItem, ScaledIngredientResult } from '../utils/scalingEngine';
import { useRecipe } from '../context/RecipeContext';

interface Ingredient {
  name: string;
  quantity?: string | number;
  unit?: string;
  notes?: string;
}

interface ServingAdjusterProps {
  initialServings?: number;
  ingredients: (Ingredient | string)[];
  recipeTitle: string;
}

export default function ServingAdjuster({
  initialServings = 2,
  ingredients = [],
  recipeTitle,
}: ServingAdjusterProps) {
  const [servings, setServings] = useState<number>(initialServings > 0 ? initialServings : 2);
  const [copied, setCopied] = useState<boolean>(false);
  const { excludedPantryIds, togglePantryExclusion, servingsMultiplier, setServingsMultiplier } = useRecipe();

  const baseServings = initialServings > 0 ? initialServings : 2;
  const scaleFactor = servings / baseServings;

  const adjustServings = (delta: number) => {
    const nextServings = Math.min(12, Math.max(1, servings + delta));
    setServings(nextServings);
    setServingsMultiplier(nextServings / baseServings);
  };

  // Scaled ingredient items using scalingEngine
  const scaledItems: ScaledIngredientResult[] = ingredients.map((item, idx) =>
    scaleIngredientItem(item as any, idx, baseServings, servings, excludedPantryIds)
  );

  const handleCopyClipboard = () => {
    const textLines = [
      `🍽️ ${recipeTitle} (Scaled to ${servings} Servings)`,
      `──────────────────────────────`,
      ...scaledItems
        .filter((it) => !it.isExcluded)
        .map((it) => `• ${it.scaledText}`),
      `──────────────────────────────`,
      `Extracted via Universal Pro AI`,
    ];
    navigator.clipboard.writeText(textLines.join('\n')).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    });
  };

  return (
    <div style={{ marginTop: '1.25rem', marginBottom: '1.25rem' }}>
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          padding: '0.75rem 1rem',
          background: 'rgba(255, 255, 255, 0.03)',
          border: '1px solid var(--border-subtle)',
          borderRadius: 'var(--radius-sm)',
          marginBottom: '1rem',
          flexWrap: 'wrap',
          gap: '0.75rem',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <Users size={18} color="var(--accent-emerald)" />
          <span style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>Serving Yield:</span>
          <span style={{ fontSize: '1rem', fontWeight: 700, color: 'var(--text-primary)' }} className="tabular-num">
            {servings} {servings === 1 ? 'Person' : 'People'}
          </span>
          {servings !== initialServings && (
            <span style={{ fontSize: '0.75rem', color: 'var(--accent-amber)' }} className="tabular-num">
              ({(scaleFactor * 100).toFixed(0)}% scale)
            </span>
          )}
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <button
            onClick={() => adjustServings(-1)}
            disabled={servings <= 1}
            className="btn-ghost chip-tactile"
            style={{ padding: '0.35rem 0.65rem', borderRadius: '6px' }}
            title="Decrease Servings"
          >
            <Minus size={14} />
          </button>
          <span style={{ minWidth: '24px', textAlign: 'center', fontWeight: 600 }} className="tabular-num">{servings}</span>
          <button
            onClick={() => adjustServings(1)}
            disabled={servings >= 12}
            className="btn-ghost chip-tactile"
            style={{ padding: '0.35rem 0.65rem', borderRadius: '6px' }}
            title="Increase Servings"
          >
            <Plus size={14} />
          </button>

          <button
            onClick={handleCopyClipboard}
            className="btn-ghost chip-tactile"
            style={{ marginLeft: '0.5rem', padding: '0.35rem 0.75rem' }}
            title="Copy scaled recipe"
          >
            {copied ? (
              <>
                <Check size={14} color="var(--accent-emerald)" />
                <span style={{ color: 'var(--accent-emerald)', fontSize: '0.8rem' }}>Copied!</span>
              </>
            ) : (
              <>
                <Copy size={14} />
                <span style={{ fontSize: '0.8rem' }}>Copy Scaled</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* Ingredient Grid with 1-click Quick Commerce Purchase */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
        {scaledItems.map((item, idx) => {
          const searchParam = encodeURIComponent(item.cleanName);
          const amazonUrl = `/api/v1/affiliate/redirect?platform=amazon&query=${searchParam}`;
          const zeptoUrl = `/api/v1/affiliate/redirect?platform=zepto&query=${searchParam}`;

          return (
            <div
              key={idx}
              className="accent-border-t-cyan"
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                padding: '0.55rem 0.85rem',
                background: 'rgba(255, 255, 255, 0.02)',
                border: '1px solid rgba(255, 255, 255, 0.04)',
                borderRadius: '8px',
                fontSize: '0.9rem',
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem' }}>
                <span
                  style={{
                    width: '6px',
                    height: '6px',
                    borderRadius: '50%',
                    background: 'var(--accent-emerald)',
                    display: 'inline-block',
                  }}
                />
                <span>
                  {item.displayQty && (
                    <strong style={{ color: 'var(--accent-emerald)', marginRight: '0.35rem' }} className="tabular-num">
                      {item.displayQty}
                    </strong>
                  )}
                  <span style={{ color: 'var(--text-primary)' }}>{item.name}</span>
                </span>
              </div>

              {/* Quick Commerce Affiliate Buy Pills */}
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
                <a
                  href={amazonUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="chip-tactile"
                  style={{
                    display: 'inline-flex',
                    alignItems: 'center',
                    gap: '0.25rem',
                    fontSize: '0.72rem',
                    padding: '0.2rem 0.5rem',
                    background: 'rgba(245, 158, 11, 0.12)',
                    color: '#FCD34D',
                    border: '1px solid rgba(245, 158, 11, 0.3)',
                    borderRadius: '4px',
                    textDecoration: 'none',
                    fontWeight: 600,
                  }}
                  title={`Order ${item.cleanName} on Amazon`}
                >
                  <ShoppingCart size={11} />
                  <span>Amazon</span>
                </a>

                <a
                  href={zeptoUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="chip-tactile"
                  style={{
                    display: 'inline-flex',
                    alignItems: 'center',
                    gap: '0.25rem',
                    fontSize: '0.72rem',
                    padding: '0.2rem 0.5rem',
                    background: 'rgba(236, 72, 153, 0.12)',
                    color: '#F472B6',
                    border: '1px solid rgba(236, 72, 153, 0.3)',
                    borderRadius: '4px',
                    textDecoration: 'none',
                    fontWeight: 600,
                  }}
                  title={`10-min delivery on Zepto`}
                >
                  <span>⚡ Zepto</span>
                </a>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
