export interface ParsedDuration {
  label: string;
  seconds: number;
  startIndex: number;
  endIndex: number;
}

/**
 * Deterministic Regex Duration Tokenizer (SAFE-1105)
 * ===================================================
 * Scans cooking & instruction text to extract time durations
 * (e.g., "simmer for 15-20 mins", "bake for 1 hr 30 min", "whisk for 45 secs")
 * into structured second bounds with zero secondary LLM latency.
 */
export function parseInstructionDurations(text: string): ParsedDuration[] {
  if (!text) return [];

  const results: ParsedDuration[] = [];

  // Match pattern examples:
  // "10-15 mins", "15 to 20 minutes", "1 hr 30 min", "45 seconds", "2.5 hours", "1.5 hrs"
  const durationRegex =
    /\b(?:(\d+(?:\.\d+)?)\s*(?:-|to)\s*)?(\d+(?:\.\d+)?)\s*(hours?|hrs?|h|minutes?|mins?|m|seconds?|secs?|s)\b(?:(?:\s*and\s*|\s*)(?:(\d+(?:\.\d+)?)\s*(minutes?|mins?|m|seconds?|secs?|s)\b))?/gi;

  let match: RegExpExecArray | null;

  while ((match = durationRegex.exec(text)) !== null) {
    const rawMatch = match[0];
    const startIndex = match.index;
    const endIndex = startIndex + rawMatch.length;

    const lowerUnit1 = (match[3] || '').toLowerCase();
    const val1 = parseFloat(match[2]);
    const rangeLower = match[1] ? parseFloat(match[1]) : null;

    // Use upper bound or primary value for countdowns
    const targetVal = rangeLower !== null ? Math.max(rangeLower, val1) : val1;

    let totalSeconds = 0;

    if (lowerUnit1.startsWith('h')) {
      totalSeconds += targetVal * 3600;
      if (match[4] && match[5]) {
        const val2 = parseFloat(match[4]);
        const lowerUnit2 = match[5].toLowerCase();
        if (lowerUnit2.startsWith('m')) {
          totalSeconds += val2 * 60;
        } else if (lowerUnit2.startsWith('s')) {
          totalSeconds += val2;
        }
      }
    } else if (lowerUnit1.startsWith('m')) {
      totalSeconds += targetVal * 60;
    } else if (lowerUnit1.startsWith('s')) {
      totalSeconds += targetVal;
    }

    if (totalSeconds > 0) {
      results.push({
        label: rawMatch.trim(),
        seconds: Math.round(totalSeconds),
        startIndex,
        endIndex,
      });
    }
  }

  return results;
}
