"""
Sprint 12 Interactive Hands-Free Cooking Mode Test Suite
========================================================
Tests Fullscreen CookingModeDrawer component structure, wake lock binding,
step timer integration, recipe context hooks, and Web Speech API voice bridge.
"""

import unittest
from pathlib import Path


class TestSprint12CookingMode(unittest.TestCase):
    def setUp(self):
        self.root_dir = Path(__file__).resolve().parent.parent
        self.drawer_file = self.root_dir / "frontend" / "src" / "components" / "CookingModeDrawer.tsx"
        self.page_file = self.root_dir / "frontend" / "src" / "app" / "page.tsx"

    def test_cooking_mode_drawer_component_exists(self):
        """Verify frontend/src/components/CookingModeDrawer.tsx exists and exports default function."""
        self.assertTrue(self.drawer_file.exists(), "Missing CookingModeDrawer.tsx component")
        content = self.drawer_file.read_text(encoding="utf-8")

        self.assertIn("export default function CookingModeDrawer", content)
        self.assertIn("export interface CookingModeDrawerProps", content)

    def test_wake_lock_integration_in_drawer(self):
        """Verify CookingModeDrawer binds useWakeLock and auto-requests screen wake lock."""
        content = self.drawer_file.read_text(encoding="utf-8")

        self.assertIn("useWakeLock()", content)
        self.assertIn("requestWakeLock()", content)
        self.assertIn("releaseWakeLock()", content)
        self.assertIn("Screen Awake", content)

    def test_step_timer_integration_in_drawer(self):
        """Verify CookingModeDrawer integrates parseInstructionDurations and useStepTimer."""
        content = self.drawer_file.read_text(encoding="utf-8")

        self.assertIn("parseInstructionDurations", content)
        self.assertIn("useStepTimer", content)
        self.assertIn("remainingSeconds", content)
        self.assertIn("startTimer", content)
        self.assertIn("pauseTimer", content)
        self.assertIn("resetTimer", content)

    def test_recipe_context_integration_in_drawer(self):
        """Verify CookingModeDrawer accesses RecipeContext for ingredient check marks and servings."""
        content = self.drawer_file.read_text(encoding="utf-8")

        self.assertIn("useRecipe()", content)
        self.assertIn("checkedIngredientIds", content)
        self.assertIn("toggleIngredientCheck", content)

    def test_voice_navigation_bridge_in_drawer(self):
        """Verify CookingModeDrawer implements Web Speech API voice recognition fallback."""
        content = self.drawer_file.read_text(encoding="utf-8")

        self.assertIn("SpeechRecognition", content)
        self.assertIn("webkitSpeechRecognition", content)
        self.assertIn("transcript.includes('next')", content)
        self.assertIn("transcript.includes('back')", content)
        self.assertIn("transcript.includes('timer')", content)

    def test_keyboard_and_touch_gesture_navigation(self):
        """Verify keyboard Arrow/Space/Escape and touch swipe gesture handlers exist."""
        content = self.drawer_file.read_text(encoding="utf-8")

        self.assertIn("ArrowRight", content)
        self.assertIn("ArrowLeft", content)
        self.assertIn("Escape", content)
        self.assertIn("onTouchStart", content)
        self.assertIn("onTouchEnd", content)

    def test_page_tsx_renders_cooking_mode_drawer(self):
        """Verify frontend/src/app/page.tsx imports and renders CookingModeDrawer."""
        content = self.page_file.read_text(encoding="utf-8")

        self.assertIn("import CookingModeDrawer", content)
        self.assertIn("isCookingDrawerOpen", content)
        self.assertIn("Start Cooking Mode", content)
        self.assertIn("<CookingModeDrawer", content)


if __name__ == "__main__":
    unittest.main()
