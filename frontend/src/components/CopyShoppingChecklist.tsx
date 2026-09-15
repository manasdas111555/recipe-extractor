"use client";

import React, { useState } from "react";
import { Clipboard, Check } from "lucide-react";

interface Ingredient {
  name?: string;
  amount?: string;
  quantity?: string;
  unit?: string;
}

interface CopyShoppingChecklistProps {
  recipeTitle: string;
  servings?: number;
  ingredients: Ingredient[];
}

export default function CopyShoppingChecklist({
  recipeTitle,
  servings = 2,
  ingredients = [],
}: CopyShoppingChecklistProps) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    const listText = ingredients
      .map((item) => {
        if (typeof item === "string") return `• ${item}`;
        const qty = item.amount || item.quantity || "";
        const u = item.unit || "";
        const measure = `${qty} ${u}`.trim();
        const name = item.name || "";
        return `• ${measure ? measure + " " : ""}${name}`.trim();
      })
      .join("\n");

    const payload = `🛒 ${recipeTitle} (${servings} servings)\nIngredients Checklist:\n${listText}\n\n⚡ Extracted via Universal Pro AI`;

    let success = false;

    // 1. Try Modern Async Clipboard API
    if (navigator.clipboard && window.isSecureContext) {
      try {
        await navigator.clipboard.writeText(payload);
        success = true;
      } catch (err) {
        console.warn("Async clipboard failed, attempting fallback...", err);
      }
    }

    // 2. Fallback for iOS Safari & In-App WebViews
    if (!success) {
      try {
        const textArea = document.createElement("textarea");
        textArea.value = payload;
        textArea.style.position = "fixed";
        textArea.style.left = "-999999px";
        textArea.style.top = "-999999px";
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        success = document.execCommand("copy");
        document.body.removeChild(textArea);
      } catch (err) {
        console.error("All copy mechanisms failed", err);
      }
    }

    if (success) {
      setCopied(true);
      setTimeout(() => setCopied(false), 2500);
    }
  };

  return (
    <button
      onClick={handleCopy}
      className="inline-flex items-center gap-2 px-4 py-2 text-xs font-semibold rounded-lg bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/20 hover:bg-emerald-500/20 transition-all active:scale-95 cursor-pointer"
    >
      {copied ? (
        <Check className="w-3.5 h-3.5 text-emerald-500" />
      ) : (
        <Clipboard className="w-3.5 h-3.5" />
      )}
      <span>{copied ? "Copied to Clipboard!" : "📋 Copy Shopping Checklist"}</span>
    </button>
  );
}
