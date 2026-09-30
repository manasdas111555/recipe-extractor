"""
Unit test asserting that Hinglish culinary prompt rules and linguistic mappings
exist in gemini_processor.py system prompt templates (Rule 13 snapshot requirement).
"""

import sys
import os
from pathlib import Path

# Add backend app directory to sys.path
backend_dir = Path(__file__).resolve().parent.parent / "backend" / "app"
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

services_dir = backend_dir / "services"
if str(services_dir) not in sys.path:
    sys.path.insert(0, str(services_dir))

from gemini_processor import REGIONAL_EXTRACTION_SYSTEM_PROMPT

def test_hinglish_prompt_snapshot():
    """Asserts that required Hinglish metrics and culinary mappings exist in system prompt."""
    prompt = REGIONAL_EXTRACTION_SYSTEM_PROMPT

    # Assert spoken metric mappings
    assert '"1 katori" -> "1 bowl (~150 ml, approx)"' in prompt
    assert '"ek chamach" -> "1 tbsp (approx)"' in prompt
    assert '"chota chamach" -> "1 tsp (approx)"' in prompt
    assert '"chutki bhar" -> "1 pinch (approx)"' in prompt
    assert '"swadanusar" -> "to taste"' in prompt

    # Assert ingredient localization examples
    assert "Clarified Butter (Ghee)" in prompt
    assert "Cumin Seeds (Jeera)" in prompt
    assert "Dried Fenugreek (Kasuri Methi)" in prompt
    assert "Asafoetida (Hing)" in prompt

    # Assert quick-commerce search keyword guidance
    assert "Quick-Commerce Search Keywords:" in prompt
    assert "Kasuri Methi" in prompt
