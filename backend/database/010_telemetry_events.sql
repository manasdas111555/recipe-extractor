-- ============================================================================
-- Supabase PostgreSQL Migration 010: Growth Telemetry & Conversion Events
-- ============================================================================
-- Story / Ticket: UPA-1229
-- Schema Target: PostgreSQL 15+ / Supabase
-- Description: Provisions public.telemetry_events table matching exact payload schema
--              expected by backend/app/api/v1/telemetry.py & supabase_client.py.
--              Enforces strict RLS isolation & service_role grants.
-- ============================================================================

-- 1. Create Telemetry Events Table
CREATE TABLE IF NOT EXISTS public.telemetry_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_name TEXT NOT NULL CHECK (event_name IN (
        'video_shared',
        'extraction_rendered',
        'affiliate_outbound_clicked',
        'paywall_hit',
        'subscription_converted'
    )),
    user_id TEXT, -- TEXT required to support both guest_... session strings and UUIDs
    session_id TEXT,
    properties JSONB NOT NULL DEFAULT '{}'::jsonb, -- Must be 'properties', matching payload key
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- 2. Performance Indexes
CREATE INDEX IF NOT EXISTS idx_telemetry_events_created ON public.telemetry_events (created_at DESC);
CREATE INDEX IF NOT EXISTS idx_telemetry_events_name_created ON public.telemetry_events (event_name, created_at DESC);

-- 3. Row Level Security (RLS) & Grant Isolation
ALTER TABLE public.telemetry_events ENABLE ROW LEVEL SECURITY;

-- Grant access ONLY to service_role (FastAPI backend uses service_role_key)
GRANT ALL ON public.telemetry_events TO service_role;
REVOKE ALL ON public.telemetry_events FROM anon, authenticated;

-- RLS Policies strictly scoped to service_role
CREATE POLICY "Service role insert telemetry events"
    ON public.telemetry_events FOR INSERT
    TO service_role
    WITH CHECK (true);

CREATE POLICY "Service role read telemetry events"
    ON public.telemetry_events FOR SELECT
    TO service_role
    USING (true);
