-- ============================================================================
-- UNIVERSAL PRO AI — MIGRATION 012: EXTRACTION PUBLIC OWNERSHIP & VISIBILITY
-- ============================================================================
-- Story / Ticket: UPA-1215
-- Schema Target: PostgreSQL 15+ / Supabase
-- Purpose: Formalizes the public vs private ownership data contract on public.extractions.
--          Enforces that anonymous/guest users can only access rows where is_public = true,
--          while authenticated users can access their own rows (user_id = auth.uid())
--          or public rows. Adds performance indexes for ownership and visibility filtering.
-- Predecessor Migrations Required: 001_initial_schema.sql, 011_privilege_hardening.sql
-- Execution Scope: DDL specification only. DO NOT EXECUTE DIRECTLY during dev testing.
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 1. COLUMN DEFAULT & NOT NULL ASSURANCES
-- ----------------------------------------------------------------------------
DO $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_schema = 'public' 
          AND table_name = 'extractions' 
          AND column_name = 'is_public'
    ) THEN
        -- Ensure default is FALSE for newly created private extractions
        ALTER TABLE public.extractions ALTER COLUMN is_public SET DEFAULT false;
        ALTER TABLE public.extractions ALTER COLUMN is_public SET NOT NULL;
    END IF;
END $$;

-- ----------------------------------------------------------------------------
-- 2. DEDICATED VISIBILITY & OWNERSHIP INDEXES
-- ----------------------------------------------------------------------------
CREATE INDEX IF NOT EXISTS idx_extractions_is_public 
    ON public.extractions (is_public);

CREATE INDEX IF NOT EXISTS idx_extractions_user_public 
    ON public.extractions (user_id, is_public);

CREATE INDEX IF NOT EXISTS idx_extractions_id_is_public
    ON public.extractions (id, is_public);

-- ----------------------------------------------------------------------------
-- 3. RLS POLICY SPECIFICATION CONTRACT
-- ----------------------------------------------------------------------------
-- Anonymous users: SELECT allowed ONLY when is_public = true
-- Authenticated users: SELECT allowed when user_id = auth.uid() OR is_public = true
-- Service role: Full access bypass via service_role key

ALTER TABLE public.extractions ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Public extractions viewable by anyone" ON public.extractions;
CREATE POLICY "Public extractions viewable by anyone" 
    ON public.extractions 
    FOR SELECT 
    USING (is_public = true);

DROP POLICY IF EXISTS "Users view own extractions" ON public.extractions;
CREATE POLICY "Users view own extractions" 
    ON public.extractions 
    FOR SELECT 
    TO authenticated 
    USING (user_id = auth.uid() OR is_public = true);
