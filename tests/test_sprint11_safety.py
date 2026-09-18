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


if __name__ == "__main__":
    unittest.main()
