'use client';

import React, { useState } from 'react';
import { Users, Minus, Plus, ShoppingCart, Copy, Check } from 'lucide-react';

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

/**
 * Parses numeric value or simple fraction from an ingredient quantity string
 */
function parseQuantity(qty: string | number | undefined): number | null {
  if (qty === undefined || qty === null) return null;
  if (typeof qty === 'number') return qty;
  const str = qty.trim();
  if (!str) return null;

  // Check fraction like 1/2, 3/4
  if (str.includes('/')) {
    const parts = str.split('/');
    if (parts.length === 2) {
      const num = parseFloat(parts[0]);
      const den = parseFloat(parts[1]);
      if (!isNaN(num) && !isNaN(den) && den !== 0) {
        return num / den;
      }
    }
  }

  // Range like 2-3 (use average or first)
  if (str.includes('-')) {
    const parts = str.split('-');
    const first = parseFloat(parts[0]);
    if (!isNaN(first)) return first;
  }

  const num = parseFloat(str);
  return isNaN(num) ? null : num;
}

/**
 * Formats scaled quantity cleanly (e.g. 1.5 -> 1 1/2 or 1.5)
 */
function formatQuantity(val: number): string {
  if (Math.abs(val - Math.round(val)) < 0.05) {
    return Math.round(val).toString();
  }
  // Check common fractions
  const whole = Math.floor(val);
  const frac = val - whole;
  if (Math.abs(frac - 0.5) < 0.05) return whole > 0 ? `${whole} ½` : '½';
  if (Math.abs(frac - 0.25) < 0.05) return whole > 0 ? `${whole} ¼` : '¼';
  if (Math.abs(frac - 0.75) < 0.05) return whole > 0 ? `${whole} ¾` : '¾';
  if (Math.abs(frac - 0.33) < 0.06) return whole > 0 ? `${whole} ⅓` : '⅓';
  if (Math.abs(frac - 0.67) < 0.06) return whole > 0 ? `${whole} ⅔` : '⅔';

  return val.toFixed(1).replace(/\.0$/, '');
}

export default function ServingAdjuster({
  initialServings = 2,
  ingredients = [],
  recipeTitle,
}: ServingAdjusterProps) {
  const [servings, setServings] = useState<number>(initialServings > 0 ? initialServings : 2);
  const [copied, setCopied] = useState<boolean>(false);

  const scaleFactor = servings / (initialServings > 0 ? initialServings : 2);

  const adjustServings = (delta: number) => {
    setServings((prev) => Math.min(12, Math.max(1, prev + delta)));
  };

  // Scaled ingredient list
  const scaledItems = ingredients.map((item) => {
    if (typeof item === 'string') {
      // Attempt regex extract if string starts with a number
      const match = item.match(/^([\d\/\.\-]+)\s*([a-zA-Z]+)?\s*(.*)$/);
      if (match) {
        const parsed = parseQuantity(match[1]);
        if (parsed !== null) {
          const scaled = parsed * scaleFactor;
          const unit = match[2] || '';
          const rest = match[3] || '';
          return {
            name: `${unit} ${rest}`.trim(),
            displayQty: formatQuantity(scaled),
            rawItem: `${formatQuantity(scaled)} ${unit} ${rest}`.trim(),
            cleanName: rest || unit || item,
          };
        }
      }
      return {
        name: item,
        displayQty: '',
        rawItem: item,
        cleanName: item,
      };
    } else {
      const parsed = parseQuantity(item.quantity);
      const displayQty = parsed !== null ? formatQuantity(parsed * scaleFactor) : item.quantity ? String(item.quantity) : '';
      const unit = item.unit || '';
      return {
        name: `${unit} ${item.name}`.trim(),
        displayQty,
        rawItem: `${displayQty} ${unit} ${item.name}`.trim(),
        cleanName: item.name,
      };
    }
  });

  const handleCopyClipboard = () => {
    const textLines = [
      `🍽️ ${recipeTitle} (Scaled to ${servings} Servings)`,
      `──────────────────────────────`,
      ...scaledItems.map((it) => `• ${it.rawItem}`),
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
          <span style={{ fontSize: '1rem', fontWeight: 700, color: 'var(--text-primary)' }}>
            {servings} {servings === 1 ? 'Person' : 'People'}
          </span>
          {servings !== initialServings && (
            <span style={{ fontSize: '0.75rem', color: 'var(--accent-amber)' }}>
              ({(scaleFactor * 100).toFixed(0)}% scale)
            </span>
          )}
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <button
            onClick={() => adjustServings(-1)}
            disabled={servings <= 1}
            className="btn-ghost"
            style={{ padding: '0.35rem 0.65rem', borderRadius: '6px' }}
            title="Decrease Servings"
          >
            <Minus size={14} />
          </button>
          <span style={{ minWidth: '24px', textAlign: 'center', fontWeight: 600 }}>{servings}</span>
          <button
            onClick={() => adjustServings(1)}
            disabled={servings >= 12}
            className="btn-ghost"
            style={{ padding: '0.35rem 0.65rem', borderRadius: '6px' }}
            title="Increase Servings"
          >
            <Plus size={14} />
          </button>

          <button
            onClick={handleCopyClipboard}
            className="btn-ghost"
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
                    <strong style={{ color: 'var(--accent-emerald)', marginRight: '0.35rem' }}>
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
