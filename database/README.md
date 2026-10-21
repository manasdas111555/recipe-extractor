# 🗄️ Universal Pro AI — Database Deployment & Migration Guide

This directory contains the canonical PostgreSQL 15+ database migration scripts for **Universal Pro AI** hosted on **Supabase**.

---

## 📁 Migration Files & Replay Sequence

Migrations must be executed in strict sequential order:

| Migration | File | Epics / Tickets Covered | Description & Access Controls |
| :--- | :--- | :--- | :--- |
| **001** | `001_initial_schema.sql` | `UPA-101`, `UPA-102`, `UPA-103`, `UPA-1406` | Core tables (`profiles`, `extractions`, `affiliate_clicks`), RLS policies, SHA-256 URL hash caching index, user profile triggers, schema usage (`GRANT USAGE`), explicit least-privilege Data API grants, and function search-path hardening. |
| **009** | `009_beta_telemetry_feed.sql` | `UPA-902`, `UPA-1406` | Beta telemetry & observability feed table (`beta_telemetry_feed`), timestamp indexing, RLS policies, and explicit `service_role` `INSERT` grant. |
| **010** | `010_telemetry_events.sql` | `UPA-1229`, `UPA-1406` | Product telemetry events table (`telemetry_events`), composite timestamp indexes, RLS isolation, and explicit `service_role` `SELECT, INSERT` grants. |
| **011** | `011_privilege_hardening.sql` | `UPA-1230`, `UPA-1406` | Idempotent minimum-privilege security hardening for existing environments: schema creation revocation, table grant enforcement across all 5 tables, search-path isolation (`SET search_path = public, pg_temp`), and RPC function execution restrictions for reviewed functions. |
| **012** | `012_extraction_public_ownership.sql` | `UPA-1215`, `UPA-1406` | Data contract formalization for public vs private extraction ownership on `public.extractions`, RLS policies, column defaults, and dedicated composite visibility indexes. |

---

## 🚀 Environment Deployment Runbook

### Scenario A: Fresh Environment Provisioning (New Supabase Project / Local PostgreSQL)
When standing up a fresh environment (e.g. disaster recovery rebuild or local development container):
1. Execute migrations in exact sequential order:
   - `001_initial_schema.sql`
   - `009_beta_telemetry_feed.sql`
   - `010_telemetry_events.sql`
   - `011_privilege_hardening.sql`
   - `012_extraction_public_ownership.sql`
2. Migration `001` now includes explicit table grants, schema usage, and function protections so that the environment is fully operational post-October 30, 2026 without relying on Supabase's legacy automatic table grants.
3. Subsequent migrations (`009` through `012`) incrementally apply subsequent tables, explicit grants, security policies, and ownership indexes.

### Scenario B: Existing Deployed Environments (Staging / Production)
> [!IMPORTANT]
> **DO NOT RERUN MIGRATION 001** against an existing environment merely to apply grants or security hardening.
> Re-running initial schema DDL against live databases can cause unintended locks or drop conflicts.
1. In existing environments that already have `001`, `009`, and `010` applied, apply **`011_privilege_hardening.sql`** and **`012_extraction_public_ownership.sql`** as forward-only, idempotent migrations.
2. `011_privilege_hardening.sql` explicitly revokes legacy broad privileges, establishes minimum-privilege grants on all 5 application tables, sets function search_paths, and restricts RPC execution without mutating schema structure or data.
3. Every execution against Staging must be governed by Rule 2 and Tier 1 live smoke verification. Production execution is strictly prohibited without explicit, written Product Owner authorization in `SIGN_OFF.md`.

---

## 🛡️ Security & Access Control Contract

- **Zero Direct PostgreSQL Wire Connections**: The application connects exclusively through Supabase's PostgREST HTTP Data API (`/rest/v1/`). Table-level and schema-level `GRANT` statements dictate API availability.
- **Least-Privilege Role Mapping**:
  - `service_role`: Used exclusively by the backend API and Celery workers with `SUPABASE_SERVICE_ROLE_KEY`. Granted table permissions strictly needed for operations (`SELECT, UPDATE` on `profiles`; `SELECT, INSERT, DELETE` on `extractions`; `SELECT, INSERT` on `affiliate_clicks` and `telemetry_events`; `INSERT` on `beta_telemetry_feed`).
  - `anon` / `authenticated`: Granted `SELECT` on `extractions` subject to Row Level Security (`is_public = true` or `user_id = auth.uid()`). No write permissions granted to client roles.
  - `PUBLIC`: All function execution revoked on reviewed application functions (`increment_user_extraction_count`, `reset_daily_extraction_quotas`, `handle_new_user`).
- **Function Search-Path Protection**: Reviewed `SECURITY DEFINER` functions explicitly enforce `SET search_path = public, pg_temp` to prevent search-path hijacking attacks.
- **Disaster Recovery Distinction**:
  - *Schema Rebuild Readiness*: The migration chain `001 -> 012` deterministically rebuilds the complete schema DDL, RLS policies, and Data API grant matrix from scratch.
  - *Independent Data Recovery*: Restoring user profiles, historical extractions, and analytics requires external encrypted backups (`pg_dump` schema + data) and independent Supabase Storage object backups.
