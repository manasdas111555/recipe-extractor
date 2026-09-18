"""
Sprint 11 Safety & Architectural Groundwork Test Suite
======================================================
Tests TypeScript null-safety schema definitions, historical extraction backwards compatibility,
and defensive infrastructure hooks.
"""

import unittest
from pathlib import Path


class TestSprint11SafetySchema(unittest.TestCase):
    def setUp(self):
        self.root_dir = Path(__file__).resolve().parent.parent
        self.types_file = self.root_dir / "frontend" / "src" / "types" / "recipe.ts"

    def test_recipe_types_file_exists(self):
        """Verify that frontend/src/types/recipe.ts exists and contains NutritionInfo."""
        self.assertTrue(self.types_file.exists(), "Missing frontend/src/types/recipe.ts")
        content = self.types_file.read_text(encoding="utf-8")
        
        self.assertIn("export interface NutritionInfo", content)
        self.assertIn("calories?: number", content)
        self.assertIn("protein_g?: number", content)
        self.assertIn("carbs_g?: number", content)
        self.assertIn("fat_g?: number", content)
        self.assertIn("is_estimated?: boolean", content)

    def test_extraction_result_includes_optional_nutrition(self):
        """Verify ExtractionResult type interface includes optional nutrition property."""
        content = self.types_file.read_text(encoding="utf-8")
        self.assertIn("nutrition?: NutritionInfo;", content)
        self.assertIn("export type RecipeSchema = ExtractionResult;", content)


    def test_use_wake_lock_hook_exists(self):
        """Verify that frontend/src/hooks/useWakeLock.ts exists and handles visibilitychange."""
        hook_file = self.root_dir / "frontend" / "src" / "hooks" / "useWakeLock.ts"
        self.assertTrue(hook_file.exists(), "Missing frontend/src/hooks/useWakeLock.ts")
        content = hook_file.read_text(encoding="utf-8")
        
        self.assertIn("export function useWakeLock(): UseWakeLockReturn", content)
        self.assertIn("'wakeLock' in navigator", content)
        self.assertIn("visibilitychange", content)
        self.assertIn("wakeLockSentinelRef.current.release()", content)


    def test_use_step_timer_hook_exists(self):
        """Verify that frontend/src/hooks/useStepTimer.ts exists and implements delta math + Web Audio."""
        hook_file = self.root_dir / "frontend" / "src" / "hooks" / "useStepTimer.ts"
        self.assertTrue(hook_file.exists(), "Missing frontend/src/hooks/useStepTimer.ts")
        content = hook_file.read_text(encoding="utf-8")
        
        self.assertIn("export function useStepTimer({ durationSeconds, onComplete }: UseStepTimerOptions): UseStepTimerReturn", content)
        self.assertIn("targetEndTimeRef.current = Date.now() + remainingSeconds * 1000", content)
        self.assertIn("AudioContext", content)
        self.assertIn("vibrate", content)


    def test_recipe_context_store_exists(self):
        """Verify that frontend/src/context/RecipeContext.tsx exists and exposes context provider."""
        context_file = self.root_dir / "frontend" / "src" / "context" / "RecipeContext.tsx"
        self.assertTrue(context_file.exists(), "Missing frontend/src/context/RecipeContext.tsx")
        content = context_file.read_text(encoding="utf-8")
        
        self.assertIn("export const RecipeProvider", content)
        self.assertIn("servingsMultiplier", content)
        self.assertIn("checkedIngredientIds", content)
        self.assertIn("excludedPantryIds", content)
        self.assertIn("getFilteredIngredients", content)


    def test_duration_parser_utility_exists(self):
        """Verify that frontend/src/utils/durationParser.ts exists and exports parseInstructionDurations."""
        parser_file = self.root_dir / "frontend" / "src" / "utils" / "durationParser.ts"
        self.assertTrue(parser_file.exists(), "Missing frontend/src/utils/durationParser.ts")
        content = parser_file.read_text(encoding="utf-8")
        
        self.assertIn("export function parseInstructionDurations(text: string): ParsedDuration[]", content)
        self.assertIn("durationRegex", content)
        self.assertIn("totalSeconds", content)


if __name__ == "__main__":
    unittest.main()




