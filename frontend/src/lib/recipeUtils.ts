/**
 * Pure Recipe & Extraction Utility Functions (UPA-Frontend-Pure)
 * =============================================================
 * Self-contained pure functions operating solely on explicit arguments.
 * No closure variables, no side effects.
 */

export interface MediaPreview {
  type: 'video' | 'instagram' | 'youtube' | 'tiktok';
  src?: string;
  streamSrc?: string;
  embedSrc?: string;
  externalUrl?: string;
  id?: string;
}

/**
 * Resolves media preview target for direct video, Instagram Reel iframe, YouTube, or TikTok.
 */
export function resolveMediaPreview(result: any, fallbackUrl?: string): MediaPreview | null {
  const target = result?.source_url || (result as any)?.media_url || fallbackUrl;
  if (!target) return null;

  // 1. Direct video link (mp4, webm, etc.)
  if (result?.media_url && (result.media_url.endsWith('.mp4') || result.media_url.endsWith('.webm') || result.media_url.includes('/video/'))) {
    return {
      type: 'video',
      src: result.media_url,
    };
  }

  // 2. Instagram Reel or Post: /reel/{id} or /p/{id}
  const igMatch = target.match(/instagram\.com\/(?:reel|p|tv)\/([A-Za-z0-9_-]+)/i);
  if (igMatch && igMatch[1]) {
    const token = (result as any)?.stream_token || (result as any)?.data?.stream_token || '';
    const extId = (result as any)?.job_id || (result as any)?.id || igMatch[1];
    const streamSrc = token
      ? `/api/v1/extract/stream-video?token=${encodeURIComponent(token)}&id=${encodeURIComponent(extId)}&url=${encodeURIComponent(target)}`
      : `/api/v1/extract/stream-video?url=${encodeURIComponent(target)}`;

    return {
      type: 'instagram',
      streamSrc,
      embedSrc: `https://www.instagram.com/reel/${igMatch[1]}/embed/`,
      externalUrl: `https://www.instagram.com/reel/${igMatch[1]}/`,
      id: igMatch[1],
    };
  }

  // 3. YouTube Shorts or standard YouTube video
  const ytMatch = target.match(/(?:youtube\.com\/(?:shorts\/|watch\?v=)|youtu\.be\/)([A-Za-z0-9_-]{11})/i);
  if (ytMatch && ytMatch[1]) {
    return {
      type: 'youtube',
      src: `https://www.youtube-nocookie.com/embed/${ytMatch[1]}?autoplay=0&rel=0&modestbranding=1`,
      externalUrl: `https://www.youtube.com/shorts/${ytMatch[1]}`,
      id: ytMatch[1],
    };
  }

  // 4. TikTok Video
  const ttMatch = target.match(/tiktok\.com\/(?:@[^/]+\/video\/|v\/)(\d+)/i);
  if (ttMatch && ttMatch[1]) {
    return {
      type: 'tiktok',
      src: `https://www.tiktok.com/embed/v2/${ttMatch[1]}`,
      externalUrl: target,
      id: ttMatch[1],
    };
  }

  return null;
}

/**
 * Cleans leading numerics from lines while keeping words intact.
 * e.g., "1. Salt" -> "Salt", "Salt" -> "Salt"
 */
export function cleanLineLeadingNumerics(line: string): string {
  if (!line) return '';
  const clean = line.trim();
  return clean.replace(/^\d+\s*[\.\)\-]?\s*/, '').trim();
}

/**
 * Formats a clean title by removing markdown formatting and domain tags.
 */
export function formatCleanTitle(rawTitle?: string): string {
  if (!rawTitle) return '';
  return rawTitle
    .replace(/^#+\s*/, '')
    .replace(/\*{1,2}/g, '')
    .replace(/^[-\*\•]\s*/, '')
    .trim();
}

/**
 * Parses raw ingredient string into structured name, quantity, unit.
 * Keeps "all-purpose flour" intact (splits only on " - ", ":", or "(").
 */
export function parseIngredients(text: string): Array<{ name: string; quantity?: string; unit?: string }> {
  if (!text) return [];
  const lines = text.split(/\r?\n/).map(l => l.trim()).filter(Boolean);
  return lines.map(line => {
    const cleaned = cleanLineLeadingNumerics(line);
    // Split only on explicit quantity delimiters: " - ", ":", or "("
    const parts = cleaned.split(/(?:\s+-\s+|:\s*|\s*\()/);
    if (parts.length > 1) {
      return { name: parts[0].trim(), quantity: parts[1].replace(/\)$/, '').trim() };
    }
    return { name: cleaned };
  });
}

/**
 * Formats turnaround duration in milliseconds into human readable string.
 */
export function formatTurnaroundTime(ms: number): string {
  if (!ms || ms <= 0) return '0.0s';
  const sec = (ms / 1000).toFixed(1);
  return `${sec}s`;
}

/**
 * Parses recipe sections (equipment, ingredients, instructions) from meta and details text.
 */
export function parseRecipeSections(meta: any, detailsText: string = ''): {
  equipment: string[];
  ingredients: any[];
  instructions: string[];
} {
  const equipment: string[] = meta?.equipment_needed || meta?.equipment || [];
  let ingredients: any[] = meta?.ingredients || [];
  let instructions: string[] = meta?.instructions || meta?.steps || [];

  if (detailsText && (!ingredients.length || !instructions.length)) {
    const lines = detailsText.split(/\r?\n/);
    let currentMode: 'none' | 'equip' | 'ing' | 'inst' = 'none';

    for (const rawLine of lines) {
      const line = rawLine.trim();
      if (!line) continue;

      if (/equipment/i.test(line)) {
        currentMode = 'equip';
        continue;
      } else if (/ingredient/i.test(line)) {
        currentMode = 'ing';
        continue;
      } else if (/instruction|step|method|direction/i.test(line)) {
        currentMode = 'inst';
        continue;
      }

      const item = cleanLineLeadingNumerics(line);
      if (!item) continue;

      if (currentMode === 'equip' && !equipment.includes(item)) {
        equipment.push(item);
      } else if (currentMode === 'ing' && !ingredients.some(i => (typeof i === 'string' ? i : i.name) === item)) {
        ingredients.push({ name: item });
      } else if (currentMode === 'inst' && !instructions.includes(item)) {
        instructions.push(item);
      }
    }
  }

  return { equipment, ingredients, instructions };
}

/**
 * Generates formatted structured plain text or WhatsApp formatted string from metadata.
 */
export function generateStructuredText(meta: any, isWhatsApp = false): string {
  if (!meta) return '';
  const title = formatCleanTitle(meta.title || meta.recipe_title) || 'Universal AI Extraction';
  const category = (meta.category || meta.category_name || 'INTELLIGENCE').toUpperCase();
  const isRecipe = category.includes('RECIPE') || category.includes('COOK');
  const isTravel = category.includes('TRAVEL') || (meta.travel_itinerary && meta.travel_itinerary.length > 0);

  let emoji = '⚡';
  if (isRecipe) emoji = '🍳';
  else if (category.includes('PRODUCT') || category.includes('UNBOX') || category.includes('GADGET')) emoji = '🛍️';
  else if (category.includes('TUTORIAL') || category.includes('TECH') || category.includes('CODE')) emoji = '💻';
  else if (category.includes('FITNESS') || category.includes('WORKOUT')) emoji = '🏋️';
  else if (category.includes('BEAUTY') || category.includes('SKINCARE')) emoji = '✨';
  else if (isTravel) emoji = '✈️';

  const lines: string[] = [];

  if (isWhatsApp) {
    lines.push(`${emoji} *${title}*`);
    lines.push(`_${meta.category || 'Universal AI'}_ • Extracted via Universal Pro AI\n`);
  } else {
    lines.push('==================================================');
    lines.push(`${emoji} ${title} (${meta.category || 'Universal Intelligence'})`);
    lines.push('==================================================\n');
  }

  if (meta.summary) {
    lines.push(isWhatsApp ? `📋 *Summary:*\n${meta.summary}\n` : `📋 Summary:\n${meta.summary}\n`);
  }

  if (isRecipe) {
    const { equipment, ingredients, instructions } = parseRecipeSections(meta, meta.details || meta.notes_english || '');

    if (equipment && equipment.length > 0) {
      lines.push(isWhatsApp ? `🍳 *I. Equipment Needed:*` : `==================================================\n🍳 I. Equipment Needed:\n==================================================`);
      equipment.forEach((eq: string, idx: number) => {
        const letter = String.fromCharCode(97 + idx);
        lines.push(`   ${letter}. ${eq}`);
      });
      lines.push('');
    }

    if (ingredients && ingredients.length > 0) {
      lines.push(isWhatsApp ? `🥗 *II. Ingredients (with quantity):*` : `==================================================\n🥗 II. Ingredients (with quantity):\n==================================================`);
      ingredients.forEach((ing: any, idx: number) => {
        const qty = ing.quantity ? ` - ${ing.quantity}` : '';
        const unit = ing.unit ? ` ${ing.unit}` : '';
        const name = ing.name || ing;
        lines.push(`   ${idx + 1}. ${name}${qty}${unit}`);
      });
      lines.push('');
    }

    if (instructions && instructions.length > 0) {
      lines.push(isWhatsApp ? `📝 *III. Step-by-Step Instructions:*` : `==================================================\n📝 III. Step-by-Step Instructions:\n==================================================`);
      instructions.forEach((step: string, idx: number) => {
        const cleanStep = isWhatsApp ? step.replace(/\*\*/g, '*') : step.replace(/\*\*/g, '');
        lines.push(`   ${idx + 1}. ${cleanStep}`);
      });
      lines.push('');
    }
  }

  lines.push('--------------------------------------------------');
  lines.push('Generated by Universal Pro AI (https://universal-pro-ai.vercel.app)');
  return lines.join('\n');
}
