"""
Unit & Integration Tests for LLM Council 3-Stage Consensus Engine (UPA-Sprint-8)
=============================================================================
Verifies:
1. Anonymization helper maps provider outputs to neutral Model Alpha/Beta labels.
2. LLM Council parallel dispatch and graceful single-provider fallback.
3. Integration with ai_router and provider selection dispatching.
4. Schema dictionary metadata formatting.
"""

import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path

from backend.app.services.llm_council import anonymize_outputs, run_llm_council_extraction
from ai_router import route_video_intelligence, AI_PROVIDERS


class TestLLMCouncilEngine(unittest.TestCase):

    def test_ai_providers_registry_includes_council(self):
        """Verify LLM Council is registered in AI_PROVIDERS list."""
        self.assertIn("LLM Council (Multi-Provider Consensus & Peer Audit)", AI_PROVIDERS)

    def test_anonymize_outputs_mapping(self):
        """Verify provider names are masked to neutral labels to prevent brand bias."""
        mock_results = {
            "gemini": (True, "Gemini recipe text", "Gemini txt", "path/g.txt", {"title": "Recipe A"}),
            "groq": (True, "Groq recipe text", "Groq txt", "path/q.txt", {"title": "Recipe B"}),
            "mistral": (True, "Mistral recipe text", "Mistral txt", "path/m.txt", {"title": "Recipe C"})
        }

        anon_text_map, anon_json_map = anonymize_outputs(mock_results)

        self.assertIn("Model Alpha", anon_text_map)
        self.assertIn("Model Beta", anon_text_map)
        self.assertIn("Model Gamma", anon_text_map)

        self.assertEqual(anon_text_map["Model Alpha"], "Gemini txt")
        self.assertEqual(anon_text_map["Model Beta"], "Groq txt")
        self.assertEqual(anon_text_map["Model Gamma"], "Mistral txt")

    @patch("backend.app.services.llm_council.get_api_key", return_value="fake_gemini_key")
    @patch("backend.app.services.llm_council.get_mistral_api_key", return_value="fake_mistral_key")
    @patch("backend.app.services.llm_council.get_groq_api_key", return_value="fake_groq_key")
    @patch("backend.app.services.llm_council.process_video_and_generate_recipe")
    @patch("backend.app.services.llm_council.process_video_with_mistral")
    @patch("backend.app.services.llm_council.process_video_with_groq")
    @patch("gemini_processor.run_gemini_text_query")
    def test_full_llm_council_pipeline(
        self,
        mock_text_query,
        mock_groq,
        mock_mistral,
        mock_gemini,
        mock_get_groq,
        mock_get_mistral,
        mock_get_gemini
    ):
        """Verify full 3-stage consensus pipeline completes successfully."""
        mock_gemini.return_value = (True, "Gemini Summary", "# Recipe Title\nIngredients: Paneer", "file.txt", {"recipe_name": "Paneer Tikka"})
        mock_mistral.return_value = (True, "Mistral Summary", "# Recipe Title\nIngredients: Paneer, Spices", "file.txt", {"recipe_name": "Paneer Tikka"})
        mock_groq.return_value = (True, "Groq Summary", "# Recipe Title\nIngredients: Paneer", "file.txt", {"recipe_name": "Paneer Tikka"})
        mock_text_query.return_value = "Synthesized Chairman Output for Paneer Tikka"

        success, summary, txt_content, filepath, parsed_json = run_llm_council_extraction(
            video_path="dummy_video.mp4",
            custom_gemini_key="fake_key",
            custom_mistral_key="fake_key",
            custom_groq_key="fake_key"
        )

        self.assertTrue(success)
        self.assertIn("council_meta", parsed_json)
        self.assertEqual(parsed_json["council_meta"]["mode"], "3_stage_llm_council")
        self.assertEqual(len(parsed_json["council_meta"]["participating_providers"]), 3)

    @patch("backend.app.services.llm_council.get_api_key", return_value="")
    @patch("backend.app.services.llm_council.get_mistral_api_key", return_value="")
    @patch("backend.app.services.llm_council.get_groq_api_key", return_value="")
    def test_llm_council_no_keys_failure(self, mock_groq, mock_mistral, mock_gemini):
        """Verify graceful failure message when no API keys are provided."""
        success, summary, err_msg, filepath, parsed_json = run_llm_council_extraction(
            video_path="dummy_video.mp4",
            custom_gemini_key="",
            custom_mistral_key="",
            custom_groq_key=""
        )

        self.assertFalse(success)
        self.assertIn("No API keys configured", err_msg)

    @patch("backend.app.services.llm_council.run_llm_council_extraction")
    def test_ai_router_dispatches_to_council(self, mock_council):
        """Verify central router routes 'LLM Council' requests to council service."""
        mock_council.return_value = (True, "Council Output", "txt", "path", {})

        res = route_video_intelligence(
            video_path="sample.mp4",
            provider="LLM Council (Multi-Provider Consensus & Peer Audit)",
            custom_gemini_key="gem_key"
        )

        self.assertTrue(mock_council.called)
        self.assertTrue(res[0])


if __name__ == "__main__":
    unittest.main()
