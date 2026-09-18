/**
 * Dynamic Smart Recipe Scaling Engine (Sprint 13)
 * ================================================
 * Provides numeric parsing, fraction formatting, metric/imperial conversions,
 * native parenthetical term protection (AGENTS.md Rule 13), and pantry exclusion filtering.
 */

export interface IngredientItem {
  name: string;
  quantity?: string | number;
  unit?: string;
  notes?: string;
}

export interface ScaledIngredientResult {
  id: string;
  originalText: string;
  cleanName: string;
  quantity: number | null;
  displayQuantity: string;
  unit: string;
  scaledText: string;
  parentheticalNote?: string;
  isExcluded: boolean;
}

/**
 * Parses numeric values, fractions (1/2, 3/4), or ranges (2-3) from quantity inputs.
 */
export function parseQuantity(qty: string | number | undefined | null): number | null {
  if (qty === undefined || qty === null) return null;
  if (typeof qty === 'number') return isNaN(qty) ? null : qty;
  
  const str = String(qty).trim();
  if (!str) return null;

  // Fraction check: "1/2", "1 1/2", "3/4"
  if (str.includes('/')) {
    const spaceParts = str.split(/\s+/);
    if (spaceParts.length === 2 && spaceParts[1].includes('/')) {
      const whole = parseFloat(spaceParts[0]);
      const fracParts = spaceParts[1].split('/');
      const num = parseFloat(fracParts[0]);
      const den = parseFloat(fracParts[1]);
      if (!isNaN(whole) && !isNaN(num) && !isNaN(den) && den !== 0) {
        return whole + num / den;
      }
    } else {
      const parts = str.split('/');
      if (parts.length === 2) {
        const num = parseFloat(parts[0]);
        const den = parseFloat(parts[1]);
        if (!isNaN(num) && !isNaN(den) && den !== 0) {
          return num / den;
        }
      }
    }
  }

  // Range check: "2-3" or "2 - 3" -> use base value (2)
  if (str.includes('-')) {
    const parts = str.split('-');
    const first = parseFloat(parts[0]);
    if (!isNaN(first)) return first;
  }

  const num = parseFloat(str);
  return isNaN(num) ? null : num;
}

/**
 * Formats scaled numbers into clean fractions or single-decimal strings.
 */
export function formatQuantity(val: number | null): string {
  if (val === null || isNaN(val)) return '';

  if (Math.abs(val - Math.round(val)) < 0.05) {
    return Math.round(val).toString();
  }

  const whole = Math.floor(val);
  const frac = val - whole;

  if (Math.abs(frac - 0.5) < 0.05) return whole > 0 ? `${whole} ½` : '½';
  if (Math.abs(frac - 0.25) < 0.05) return whole > 0 ? `${whole} ¼` : '¼';
  if (Math.abs(frac - 0.75) < 0.05) return whole > 0 ? `${whole} ¾` : '¾';
  if (Math.abs(frac - 0.33) < 0.06) return whole > 0 ? `${whole} ⅓` : '⅓';
  if (Math.abs(frac - 0.67) < 0.06) return whole > 0 ? `${whole} ⅔` : '⅔';

  return val.toFixed(1).replace(/\.0$/, '');
}

/**
 * AGENTS.md Rule 13: Scale main quantity while preserving native terms in parentheses.
 * e.g., "1 katori (~150g) paneer" scaled by 2x -> "2 katori (~300g) paneer"
 */
export function scaleIngredientItem(
  item: IngredientItem | string,
  index: number,
  baseServings: number,
  targetServings: number,
  excludedPantryIds: string[] = []
): ScaledIngredientResult {
  const safeBase = baseServings > 0 ? baseServings : 2;
  const safeTarget = targetServings > 0 ? targetServings : 2;
  const scaleFactor = safeTarget / safeBase;
  const id = `ing-${index}`;
  const isExcluded = excludedPantryIds.includes(id);

  let rawString = '';
  let qtyValue: number | null = null;
  let unitStr = '';
  let nameStr = '';
  let parentheticalNote = '';

  if (typeof item === 'string') {
    rawString = item.trim();
  } else if (item && typeof item === 'object') {
    const qtyPart = item.quantity !== undefined ? String(item.quantity) : '';
    const unitPart = item.unit || '';
    const namePart = item.name || '';
    rawString = `${qtyPart} ${unitPart} ${namePart}`.trim();
  }

  // Extract parenthetical note if present (e.g. "(Jeera)" or "(~150g)")
  const parenMatch = rawString.match(/\(([^)]+)\)/);
  if (parenMatch) {
    parentheticalNote = parenMatch[1];
  }

  // Regex parse leading quantity and unit
  const match = rawString.match(/^([\d\/\.\-\s]+)\s*([a-zA-Z%]+)?\s*(.*)$/);
  if (match) {
    const parsed = parseQuantity(match[1]);
    if (parsed !== null) {
      qtyValue = parsed * scaleFactor;
      unitStr = match[2] || '';
      nameStr = match[3] || rawString;
    } else {
      nameStr = rawString;
    }
  } else {
    nameStr = rawString;
  }

  // Scale numeric gram/ml values inside parenthetical note if present (e.g., ~150g -> ~300g)
  let scaledParenNote = parentheticalNote;
  if (parentheticalNote && scaleFactor !== 1) {
    scaledParenNote = parentheticalNote.replace(/(\d+)\s*(g|ml|grm|gram|grams|kg)/gi, (m, pNum, pUnit) => {
      const numVal = parseFloat(pNum);
      if (!isNaN(numVal)) {
        const scaledP = Math.round(numVal * scaleFactor);
        return `${scaledP}${pUnit}`;
      }
      return m;
    });
  }

  const formattedQty = formatQuantity(qtyValue);
  let scaledText = rawString;
  if (qtyValue !== null) {
    const baseName = nameStr.replace(/\([^)]+\)/g, '').trim();
    const parenSuffix = scaledParenNote ? ` (${scaledParenNote})` : '';
    scaledText = `${formattedQty} ${unitStr} ${baseName}${parenSuffix}`.replace(/\s+/g, ' ').trim();
  }

  return {
    id,
    originalText: rawString,
    cleanName: nameStr,
    quantity: qtyValue,
    displayQuantity: formattedQty,
    unit: unitStr,
    scaledText,
    parentheticalNote: scaledParenNote,
    isExcluded,
  };
}
