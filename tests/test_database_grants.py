"""
Unit Tests for Database Grant-Readiness, Migration Replay Parity & Least Privilege (UPA-1406)
=============================================================================================
Validates:
1. Migration directory consistency: canonical backend/database/ mirrored in root database/.
2. Explicit least-privilege Data API grants for all public tables (PostgREST readiness).
3. Rejection of unsafe wildcard/broad grants to client roles (anon, authenticated, PUBLIC).
4. Schema usage grants for anon, authenticated, service_role.
5. Search-path hardening and execution restrictions narrowed strictly to reviewed functions.
6. Row Level Security (RLS) enforcement across all application tables.
7. Verification that zero SQL sequences exist (all tables use UUIDs).
"""

import re
import unittest
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
CANONICAL_DIR = ROOT_DIR / "backend" / "database"
MIRROR_DIR = ROOT_DIR / "database"

REQUIRED_MIGRATIONS = [
    "001_initial_schema.sql",
    "009_beta_telemetry_feed.sql",
    "010_telemetry_events.sql",
    "011_privilege_hardening.sql",
    "012_extraction_public_ownership.sql",
    "README.md",
]

REVIEWED_FUNCTIONS = [
    "increment_user_extraction_count",
    "reset_daily_extraction_quotas",
    "handle_new_user",
]

PUBLIC_TABLES = [
    "profiles",
    "extractions",
    "affiliate_clicks",
    "beta_telemetry_feed",
    "telemetry_events",
]


class TestDatabaseGrantsAndParity(unittest.TestCase):

    def test_migration_directory_parity(self):
        """Verify 100% file existence and content parity between backend/database and database."""
        self.assertTrue(CANONICAL_DIR.exists(), f"Missing canonical dir: {CANONICAL_DIR}")
        self.assertTrue(MIRROR_DIR.exists(), f"Missing mirror dir: {MIRROR_DIR}")

        canonical_files = sorted([f.name for f in CANONICAL_DIR.iterdir() if f.is_file()])
        mirror_files = sorted([f.name for f in MIRROR_DIR.iterdir() if f.is_file()])

        self.assertEqual(canonical_files, mirror_files, "Migration directory filenames differ!")
        for req in REQUIRED_MIGRATIONS:
            self.assertIn(req, canonical_files, f"Missing required migration file: {req}")

            canon_content = (CANONICAL_DIR / req).read_text(encoding="utf-8").replace("\r\n", "\n")
            mirror_content = (MIRROR_DIR / req).read_text(encoding="utf-8").replace("\r\n", "\n")
            self.assertEqual(
                canon_content,
                mirror_content,
                f"Content drift detected between backend/database/{req} and database/{req}!",
            )

    def test_schema_usage_grants_present(self):
        """Verify explicit GRANT USAGE ON SCHEMA public exists in migration chain."""
        sql_001 = (CANONICAL_DIR / "001_initial_schema.sql").read_text(encoding="utf-8").lower()
        sql_011 = (CANONICAL_DIR / "011_privilege_hardening.sql").read_text(encoding="utf-8").lower()

        usage_pattern = r"grant\s+usage\s+on\s+schema\s+public\s+to\s+[^;]+service_role"
        self.assertRegex(sql_001, usage_pattern, "Missing GRANT USAGE ON SCHEMA public in 001_initial_schema.sql")
        self.assertRegex(sql_011, usage_pattern, "Missing GRANT USAGE ON SCHEMA public in 011_privilege_hardening.sql")

    def test_explicit_table_grants_for_fresh_provisioning(self):
        """Verify fresh provisioning migrations (001, 009, 010) declare explicit, table-specific grants."""
        sql_001 = (CANONICAL_DIR / "001_initial_schema.sql").read_text(encoding="utf-8").lower()
        sql_009 = (CANONICAL_DIR / "009_beta_telemetry_feed.sql").read_text(encoding="utf-8").lower()
        sql_010 = (CANONICAL_DIR / "010_telemetry_events.sql").read_text(encoding="utf-8").lower()

        # profiles: service_role needs SELECT, UPDATE
        self.assertIn("grant select, update on public.profiles to service_role", sql_001)

        # extractions: service_role needs SELECT, INSERT, DELETE; client roles need SELECT
        self.assertIn("grant select, insert, delete on public.extractions to service_role", sql_001)
        self.assertIn("grant select on public.extractions to anon, authenticated", sql_001)

        # affiliate_clicks: service_role needs SELECT, INSERT
        self.assertIn("grant select, insert on public.affiliate_clicks to service_role", sql_001)

        # beta_telemetry_feed: service_role needs INSERT
        self.assertIn("grant insert on public.beta_telemetry_feed to service_role", sql_009)

        # telemetry_events: service_role needs SELECT, INSERT
        self.assertIn("grant select, insert on public.telemetry_events to service_role", sql_010)

    def test_idempotent_hardening_in_migration_011(self):
        """Verify migration 011 establishes idempotent table grants across all 5 tables."""
        sql_011 = (CANONICAL_DIR / "011_privilege_hardening.sql").read_text(encoding="utf-8").lower()

        self.assertIn("grant select, update on public.profiles to service_role", sql_011)
        self.assertIn("grant select, insert, delete on public.extractions to service_role", sql_011)
        self.assertIn("grant select on public.extractions to anon, authenticated", sql_011)
        self.assertIn("grant select, insert on public.affiliate_clicks to service_role", sql_011)
        self.assertIn("grant insert on public.beta_telemetry_feed to service_role", sql_011)
        self.assertIn("grant select, insert on public.telemetry_events to service_role", sql_011)

    def test_rejection_of_unsafe_or_wildcard_grants(self):
        """Verify rejection of blanket write grants or GRANT ALL to client roles (anon, authenticated, PUBLIC)."""
        all_sql = ""
        for req in REQUIRED_MIGRATIONS:
            if req.endswith(".sql"):
                all_sql += (CANONICAL_DIR / req).read_text(encoding="utf-8").lower() + "\n"

        # Check for dangerous wildcard grants to client roles
        unsafe_patterns = [
            r"grant\s+all\s+on\s+public\.\w+\s+to\s+[^;]*(anon|authenticated|public)",
            r"grant\s+insert\s+on\s+public\.profiles\s+to\s+[^;]*(anon|authenticated|public)",
            r"grant\s+update\s+on\s+public\.extractions\s+to\s+[^;]*(anon|authenticated|public)",
            r"grant\s+delete\s+on\s+public\.extractions\s+to\s+[^;]*(anon|authenticated|public)",
            r"grant\s+delete\s+on\s+public\.profiles\s+to\s+[^;]*(anon|authenticated|public)",
            r"grant\s+all\s+on\s+public\.telemetry_events\s+to\s+service_role",  # Must be hardened to SELECT, INSERT
        ]
        for pattern in unsafe_patterns:
            matches = re.findall(pattern, all_sql)
            self.assertEqual(len(matches), 0, f"Unsafe grant pattern matched in migration chain: {pattern}")

    def test_function_search_path_hardening(self):
        """Verify reviewed functions have explicit SET search_path = public, pg_temp."""
        sql_001 = (CANONICAL_DIR / "001_initial_schema.sql").read_text(encoding="utf-8").lower()
        sql_011 = (CANONICAL_DIR / "011_privilege_hardening.sql").read_text(encoding="utf-8").lower()

        for fn in REVIEWED_FUNCTIONS:
            search_path_pattern = rf"alter\s+function\s+public\.{fn}\([^\)]*\)\s+set\s+search_path\s*=\s*public,\s*pg_temp"
            self.assertTrue(
                re.search(search_path_pattern, sql_001) or re.search(search_path_pattern, sql_011),
                f"Missing search_path hardening for function public.{fn}",
            )

    def test_function_execute_privilege_restrictions(self):
        """Verify execute privileges on reviewed functions are revoked from PUBLIC and granted only to service_role."""
        sql_001 = (CANONICAL_DIR / "001_initial_schema.sql").read_text(encoding="utf-8").lower()
        sql_011 = (CANONICAL_DIR / "011_privilege_hardening.sql").read_text(encoding="utf-8").lower()

        for fn in ["increment_user_extraction_count", "reset_daily_extraction_quotas"]:
            revoke_pattern = rf"revoke\s+execute\s+on\s+function\s+public\.{fn}\([^\)]*\)\s+from\s+public"
            grant_pattern = rf"grant\s+execute\s+on\s+function\s+public\.{fn}\([^\)]*\)\s+to\s+service_role"

            self.assertTrue(re.search(revoke_pattern, sql_001) or re.search(revoke_pattern, sql_011), f"Missing REVOKE EXECUTE for {fn}")
            self.assertTrue(re.search(grant_pattern, sql_001) or re.search(grant_pattern, sql_011), f"Missing GRANT EXECUTE for {fn}")

        # handle_new_user should be revoked from PUBLIC (executed via trigger only)
        self.assertTrue(
            "revoke execute on function public.handle_new_user() from public" in sql_001
            or "revoke execute on function public.handle_new_user() from public" in sql_011
        )

        # Assert no blanket REVOKE EXECUTE ON ALL FUNCTIONS FROM PUBLIC exists
        self.assertNotIn("revoke execute on all functions from public", sql_001)
        self.assertNotIn("revoke execute on all functions from public", sql_011)

    def test_rls_enabled_on_all_tables(self):
        """Verify Row Level Security is explicitly enabled on all 5 public application tables."""
        all_sql = ""
        for req in REQUIRED_MIGRATIONS:
            if req.endswith(".sql"):
                all_sql += (CANONICAL_DIR / req).read_text(encoding="utf-8").lower() + "\n"

        for table in PUBLIC_TABLES:
            rls_pattern = rf"alter\s+table\s+public\.{table}\s+enable\s+row\s+level\s+security"
            self.assertRegex(all_sql, rls_pattern, f"Missing ALTER TABLE public.{table} ENABLE ROW LEVEL SECURITY")

    def test_zero_sql_sequences_in_schema(self):
        """Verify zero SQL sequences exist across all migrations (tables use UUIDs)."""
        all_sql = ""
        for req in REQUIRED_MIGRATIONS:
            if req.endswith(".sql"):
                all_sql += (CANONICAL_DIR / req).read_text(encoding="utf-8").lower() + "\n"

        self.assertNotIn("create sequence", all_sql)
        self.assertNotIn(" serial ", all_sql)
        self.assertNotIn(" bigserial ", all_sql)


if __name__ == "__main__":
    unittest.main()
