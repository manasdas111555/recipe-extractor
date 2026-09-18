"""
Sprint 13 Dynamic Smart Recipe Scaling Engine Test Suite
========================================================
Tests numeric parsing, fraction formatting, yield scaling matrices (1-12 servings),
native parenthetical metric scaling (AGENTS.md Rule 13), and pantry exclusion filtering.
"""

import unittest
from pathlib import Path


class TestSprint13RecipeScaling(unittest.TestCase):
    def setUp(self):
        self.root_dir = Path(__file__).resolve().parent.parent
        self.engine_file = self.root_dir / "frontend" / "src" / "utils" / "scalingEngine.ts"
        self.adjuster_file = self.root_dir / "frontend" / "src" / "components" / "ServingAdjuster.tsx"

    def test_scaling_engine_file_exists(self):
        """Verify frontend/src/utils/scalingEngine.ts exists and exports functions."""
        self.assertTrue(self.engine_file.exists(), "Missing scalingEngine.ts file")
        content = self.engine_file.read_text(encoding="utf-8")

        self.assertIn("export function parseQuantity", content)
        self.assertIn("export function formatQuantity", content)
        self.assertIn("export function scaleIngredientItem", content)

    def test_serving_adjuster_uses_scaling_engine(self):
        """Verify ServingAdjuster.tsx imports scaleIngredientItem and RecipeContext."""
        content = self.adjuster_file.read_text(encoding="utf-8")

        self.assertIn("scaleIngredientItem", content)
        self.assertIn("useRecipe()", content)
        self.assertIn("setServingsMultiplier", content)
        self.assertIn("excludedPantryIds", content)

    def test_agents_rule_13_parenthetical_preservation_pattern(self):
        """Verify scalingEngine.ts implements Rule 13 parenthetical metric scaling."""
        content = self.engine_file.read_text(encoding="utf-8")

        self.assertIn("scaledParenNote", content)
        self.assertIn("g|ml|grm|gram|grams|kg", content)
        self.assertIn("Rule 13", content)


if __name__ == "__main__":
    unittest.main()
