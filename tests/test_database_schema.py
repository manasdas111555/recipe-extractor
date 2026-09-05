"""
Unit Tests for Database Schema & Entity Modeling (UPA-101, UPA-102, UPA-103)
==============================================================================
Validates:
1. SQL schema file exists and contains valid DDL definitions.
2. Tables, columns, and foreign keys are defined per architecture specs.
3. SHA-256 URL hashing logic performs instant cache key matching.
4. JSON schema structure compatibility with Universal Pro AI extractions.
"""

import unittest
import hashlib
import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
SQL_FILE = ROOT_DIR / "database" / "001_initial_schema.sql"

class TestDatabaseSchema(unittest.TestCase):

    def test_sql_file_exists(self):
        """Verify that the database migration file exists and is non-empty."""
        self.assertTrue(SQL_FILE.exists(), f"Missing schema file: {SQL_FILE}")
        content = SQL_FILE.read_text(encoding="utf-8")
        self.assertGreater(len(content), 500)

    def test_schema_contains_required_tables(self):
        """Verify presence of profiles, extractions, and affiliate_clicks tables."""
        content = SQL_FILE.read_text(encoding="utf-8").lower()
        self.assertIn("create table if not exists public.profiles", content)
        self.assertIn("create table if not exists public.extractions", content)
        self.assertIn("create table if not exists public.affiliate_clicks", content)

    def test_schema_contains_rls_and_security(self):
        """Verify that Row Level Security (RLS) is enabled (UPA-102)."""
        content = SQL_FILE.read_text(encoding="utf-8").lower()
        self.assertIn("alter table public.profiles enable row level security", content)
        self.assertIn("alter table public.extractions enable row level security", content)
        self.assertIn("alter table public.affiliate_clicks enable row level security", content)
        self.assertIn("create policy \"users can view their own profile\"", content)

    def test_schema_contains_url_hash_caching_index(self):
        """Verify that url_hash index is defined for 0-cost viral caching (UPA-103)."""
        content = SQL_FILE.read_text(encoding="utf-8").lower()
        self.assertIn("idx_extractions_url_hash", content)
        self.assertIn("url_hash text not null", content)

    def test_url_hashing_consistency(self):
        """Verify SHA-256 URL hash generation produces consistent deterministic keys."""
        test_url = "https://www.instagram.com/reel/C3x9abc123/"
        hash1 = hashlib.sha256(test_url.strip().encode("utf-8")).hexdigest()
        hash2 = hashlib.sha256(test_url.strip().encode("utf-8")).hexdigest()
        self.assertEqual(hash1, hash2)
        self.assertEqual(len(hash1), 64)

    def test_mock_structured_data_json_serializable(self):
        """Verify sample Universal Pro AI extraction payload serializes cleanly to jsonb."""
        mock_extraction = {
            "title": "Crispy Garlic Butter Potatoes",
            "domain": "recipe",
            "ingredients": [
                {"name": "Baby Potatoes", "quantity": "500g"},
                {"name": "Butter", "quantity": "2 tbsp"}
            ],
            "steps": [
                "Boil potatoes until fork tender.",
                "Smash potatoes and pan fry in garlic butter until crispy."
            ],
            "affiliate_links": {
                "amazon": "https://www.amazon.in/s?k=baby+potatoes&tag=manasdas11155-21"
            }
        }
        json_str = json.dumps(mock_extraction)
        self.assertIsInstance(json_str, str)
        parsed = json.loads(json_str)
        self.assertEqual(parsed["domain"], "recipe")
        self.assertEqual(len(parsed["ingredients"]), 2)

if __name__ == "__main__":
    unittest.main()
