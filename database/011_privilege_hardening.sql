-- ============================================================================
-- UNIVERSAL PRO AI — MIGRATION 011: MINIMUM-PRIVILEGE & SECURITY HARDENING
-- ============================================================================
-- Story / Ticket: UPA-1230
-- Schema Target: PostgreSQL 15+ / Supabase
-- Purpose: Establishes deterministic minimum application table privileges,
--          hardens SECURITY DEFINER function search_paths, revokes unauthenticated
--          public RPC execute rights, and prunes unused/unscoped RLS policies.
-- Predecessor Migrations Required: 001_initial_schema.sql, 009_beta_telemetry_feed.sql, 010_telemetry_events.sql
-- Execution Scope: STAGING-FIRST EXECUTION REQUIRED. Production MUST NOT be modified at this gate.
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 1. SCHEMA USAGE & CREATION CONTROLS
-- ----------------------------------------------------------------------------
GRANT USAGE ON SCHEMA public TO anon, authenticated, service_role;
REVOKE CREATE ON SCHEMA public FROM PUBLIC, anon, authenticated, service_role;

-- ----------------------------------------------------------------------------
-- 2. DETERMINISTIC TABLE PRIVILEGE HARDENING
-- ----------------------------------------------------------------------------

-- Table 1: public.profiles
REVOKE ALL ON public.profiles FROM PUBLIC, anon, authenticated, service_role;
GRANT SELECT, UPDATE ON public.profiles TO service_role;

-- Table 2: public.extractions
REVOKE ALL ON public.extractions FROM PUBLIC, anon, authenticated, service_role;
GRANT SELECT, INSERT, DELETE ON public.extractions TO service_role;
GRANT SELECT ON public.extractions TO anon, authenticated;

-- Table 3: public.affiliate_clicks
REVOKE ALL ON public.affiliate_clicks FROM PUBLIC, anon, authenticated, service_role;
GRANT SELECT, INSERT ON public.affiliate_clicks TO service_role;

-- Table 4: public.beta_telemetry_feed
REVOKE ALL ON public.beta_telemetry_feed FROM PUBLIC, anon, authenticated, service_role;
GRANT INSERT ON public.beta_telemetry_feed TO service_role;

-- Table 5: public.telemetry_events (Hardens Migration 010 GRANT ALL)
REVOKE ALL ON public.telemetry_events FROM PUBLIC, anon, authenticated, service_role;
GRANT SELECT, INSERT ON public.telemetry_events TO service_role;

-- ----------------------------------------------------------------------------
-- 3. SECURITY DEFINER SEARCH_PATH HARDENING
-- ----------------------------------------------------------------------------
ALTER FUNCTION public.increment_user_extraction_count(uuid) SET search_path = public, pg_temp;
ALTER FUNCTION public.reset_daily_extraction_quotas() SET search_path = public, pg_temp;
ALTER FUNCTION public.handle_new_user() SET search_path = public, pg_temp;

-- ----------------------------------------------------------------------------
-- 4. RPC EXECUTE PRIVILEGE RESTRICTIONS
-- ----------------------------------------------------------------------------
REVOKE EXECUTE ON FUNCTION public.increment_user_extraction_count(uuid) FROM PUBLIC, anon, authenticated;
GRANT EXECUTE ON FUNCTION public.increment_user_extraction_count(uuid) TO service_role;

REVOKE EXECUTE ON FUNCTION public.reset_daily_extraction_quotas() FROM PUBLIC, anon, authenticated;
GRANT EXECUTE ON FUNCTION public.reset_daily_extraction_quotas() TO service_role;

REVOKE EXECUTE ON FUNCTION public.handle_new_user() FROM PUBLIC, anon, authenticated;

-- ----------------------------------------------------------------------------
-- 5. RLS POLICY PRUNING & REFINEMENT
-- ----------------------------------------------------------------------------
ALTER TABLE public.beta_telemetry_feed ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Enable read for admin" ON public.beta_telemetry_feed;
DROP POLICY IF EXISTS "Enable insert for backend" ON public.beta_telemetry_feed;
DROP POLICY IF EXISTS "Enable insert for service_role" ON public.beta_telemetry_feed;

CREATE POLICY "Enable insert for service_role"
    ON public.beta_telemetry_feed FOR INSERT
    TO service_role
    WITH CHECK (true);
