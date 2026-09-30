-- ============================================================================
-- Supabase PostgreSQL Migration 009: Beta Telemetry & Observability Feed
-- ============================================================================

-- 1. Create Telemetry & Feedback Table
create table if not exists public.beta_telemetry_feed (
  id uuid primary key default gen_random_uuid(),
  source_platform text not null, -- 'telegram', 'whatsapp', 'web'
  source_url text not null,
  classified_domain text,
  turnaround_time_ms int,
  status text not null check (status in ('completed', 'failed')),
  error_message text,
  user_reaction text check (user_reaction in ('accurate', 'missed_details', null)),
  feedback_tag text, -- 'wrong_quantities', 'missing_steps', 'bad_transcription'
  created_at timestamp with time zone default now()
);

-- 2. Performance Index on Timestamp
create index if not exists idx_beta_telemetry_created on public.beta_telemetry_feed (created_at desc);

-- 3. Row Level Security (RLS) Policies
alter table public.beta_telemetry_feed enable row level security;

create policy "Enable insert for backend" on public.beta_telemetry_feed for insert with check (true);
create policy "Enable read for admin" on public.beta_telemetry_feed for select using (true);
