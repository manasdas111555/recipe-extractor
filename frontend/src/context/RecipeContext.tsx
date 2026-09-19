import React, { createContext, useContext, useState, useCallback, ReactNode } from 'react';

/**
 * Centralized Recipe & Pantry Context Store (SAFE-1104)
 * ====================================================
 * Coordinates serving size multipliers (1 <= n <= 12), checked ingredient states,
 * and excluded pantry staples across components. Exposes getFilteredIngredients()
 * selector for synchronized quick-commerce link generation and checklist exports.
 */

export interface RecipeContextType {
  servingsMultiplier: number;
  setServingsMultiplier: (multiplier: number) => void;
  checkedIngredientIds: Set<string>;
  toggleIngredientCheck: (id: string) => void;
  excludedPantryIds: Set<string>;
  togglePantryExclusion: (id: string) => void;
  excludeDefaultPantryBasics: (ingredients: Array<{ id?: string; name: string }>) => void;
  getFilteredIngredients: <T extends { id?: string; name: string }>(ingredients: T[]) => T[];
  resetContext: () => void;
}

const RecipeContext = createContext<RecipeContextType | undefined>(undefined);

const DEFAULT_PANTRY_KEYWORDS = ['salt', 'water', 'black pepper', 'pepper', 'cooking oil', 'oil', 'sugar'];

export const RecipeProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [servingsMultiplier, setServingsMultiplierState] = useState<number>(1);
  const [checkedIngredientIds, setCheckedIngredientIds] = useState<Set<string>>(new Set());
  const [excludedPantryIds, setExcludedPantryIds] = useState<Set<string>>(new Set());

  const setServingsMultiplier = useCallback((multiplier: number) => {
    const clamped = Math.min(12, Math.max(1, multiplier));
    setServingsMultiplierState(clamped);
  }, []);

  const toggleIngredientCheck = useCallback((id: string) => {
    setCheckedIngredientIds((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  }, []);

  const togglePantryExclusion = useCallback((id: string) => {
    setExcludedPantryIds((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  }, []);

  const excludeDefaultPantryBasics = useCallback((ingredients: Array<{ id?: string; name: string }>) => {
    const idsToExclude = new Set<string>();
    ingredients.forEach((item, idx) => {
      const itemKey = item.id || `ing-${idx}-${item.name}`;
      const nameLower = item.name.toLowerCase();
      if (DEFAULT_PANTRY_KEYWORDS.some((kw) => nameLower.includes(kw))) {
        idsToExclude.add(itemKey);
      }
    });
    setExcludedPantryIds(idsToExclude);
  }, []);

  const getFilteredIngredients = useCallback(
    <T extends { id?: string; name: string }>(ingredients: T[]): T[] => {
      return ingredients.filter((item, idx) => {
        const itemKey = item.id || `ing-${idx}-${item.name}`;
        return !excludedPantryIds.has(itemKey);
      });
    },
    [excludedPantryIds]
  );

  const resetContext = useCallback(() => {
    setServingsMultiplierState(1);
    setCheckedIngredientIds(new Set());
    setExcludedPantryIds(new Set());
  }, []);

  return (
    <RecipeContext.Provider
      value={{
        servingsMultiplier,
        setServingsMultiplier,
        checkedIngredientIds,
        toggleIngredientCheck,
        excludedPantryIds,
        togglePantryExclusion,
        excludeDefaultPantryBasics,
        getFilteredIngredients,
        resetContext,
      }}
    >
      {children}
    </RecipeContext.Provider>
  );
};

export const useRecipeContext = (): RecipeContextType => {
  const context = useContext(RecipeContext);
  if (!context) {
    // Return graceful fallback defaults if used outside provider in standalone drawer previews
    return {
      servingsMultiplier: 1,
      setServingsMultiplier: () => {},
      checkedIngredientIds: new Set(),
      toggleIngredientCheck: () => {},
      excludedPantryIds: new Set(),
      togglePantryExclusion: () => {},
      excludeDefaultPantryBasics: () => {},
      getFilteredIngredients: (ing) => ing,
      resetContext: () => {},
    };
  }
  return context;
};

export const useRecipe = useRecipeContext;
