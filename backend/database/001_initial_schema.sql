-- ==============================================================================
-- UNIVERSAL PRO AI — INITIAL PRODUCTION DATABASE SCHEMA (MIGRATION 001)
-- ==============================================================================
-- Target Engine: PostgreSQL 15+ / Supabase
-- Covers Stories: UPA-101 (Tables & Relations), UPA-102 (RLS), UPA-103 (Caching Index)
-- ==============================================================================

-- 1. Enable Required Extensions
create extension if not exists "uuid-ossp";
create extension if not exists "pgcrypto";

-- ------------------------------------------------------------------------------
-- TABLE 1: public.profiles
-- Stores user accounts, subscription tiers, daily quota usage, and custom affiliate tags.
-- ------------------------------------------------------------------------------
create table if not exists public.profiles (
    id uuid references auth.users on delete cascade primary key,
    email text unique not null,
    phone_number text unique,
    full_name text,
    avatar_url text,
    plan_tier text not null default 'free' check (plan_tier in ('free', 'pro', 'business')),
    daily_quota_limit int not null default 3,
    extractions_today int not null default 0,
    last_extraction_reset timestamp with time zone default now(),
    custom_amazon_tag text,
    custom_earnkaro_id text,
    created_at timestamp with time zone default now(),
    updated_at timestamp with time zone default now()
);

-- Index for fast profile lookups
create index if not exists idx_profiles_plan_tier on public.profiles (plan_tier);
create index if not exists idx_profiles_email on public.profiles (email);

-- ------------------------------------------------------------------------------
-- TABLE 2: public.extractions
-- Stores all social video extractions, SHA-256 URL hashes (for caching), and JSON schemas.
-- ------------------------------------------------------------------------------
create table if not exists public.extractions (
    id uuid primary key default uuid_generate_v4(),
    user_id uuid references public.profiles(id) on delete set null,
    source_url text not null,
    url_hash text not null, -- SHA-256 hash of source_url for instant 0-cost cache hits
    source_platform text check (source_platform in ('instagram', 'youtube_shorts', 'youtube_video', 'tiktok', 'web_video', 'direct_upload', 'other')),
    classified_domain text not null default 'recipe', -- recipe, tech_tutorial, product_gadget, fitness_workout, travel_guide, etc.
    raw_transcript text,
    structured_data jsonb not null default '{}'::jsonb, -- Standardized Universal Pro AI schema
    status text not null default 'pending' check (status in ('pending', 'processing', 'completed', 'failed')),
    error_message text,
    processing_time_ms int,
    is_public boolean not null default true, -- Allows shareable read-only public web links
    created_at timestamp with time zone default now(),
    updated_at timestamp with time zone default now()
);

-- High-performance indexes
create index if not exists idx_extractions_url_hash on public.extractions (url_hash);
create index if not exists idx_extractions_user_id on public.extractions (user_id);
create index if not exists idx_extractions_domain on public.extractions (classified_domain);
create index if not exists idx_extractions_created_at on public.extractions (created_at desc);

-- ------------------------------------------------------------------------------
-- TABLE 3: public.affiliate_clicks
-- Tracks click-through events for Amazon, EarnKaro, Blinkit, Zepto, and Instamart.
-- ------------------------------------------------------------------------------
create table if not exists public.affiliate_clicks (
    id uuid primary key default uuid_generate_v4(),
    extraction_id uuid references public.extractions(id) on delete cascade,
    user_id uuid references public.profiles(id) on delete set null,
    merchant text not null check (merchant in ('amazon', 'flipkart', 'meesho', 'myntra', 'blinkit', 'zepto', 'instamart', 'jiomart', 'other')),
    item_name text,
    target_url text not null,
    created_at timestamp with time zone default now()
);

-- Index for merchant performance analytics
create index if not exists idx_affiliate_clicks_extraction on public.affiliate_clicks (extraction_id);
create index if not exists idx_affiliate_clicks_merchant on public.affiliate_clicks (merchant);
create index if not exists idx_affiliate_clicks_created_at on public.affiliate_clicks (created_at desc);

-- ------------------------------------------------------------------------------
-- STORED PROCEDURE / RPC: increment_user_extraction_count
-- Atomically increments the daily quota counter for a user.
-- ------------------------------------------------------------------------------
create or replace function public.increment_user_extraction_count(user_uuid uuid)
returns void as $$
begin
    update public.profiles
    set extractions_today = extractions_today + 1,
        updated_at = now()
    where id = user_uuid;
end;
$$ language plpgsql security definer;

-- ------------------------------------------------------------------------------
-- STORED PROCEDURE / RPC: reset_daily_extraction_quotas
-- Scheduled job to reset daily counters at midnight UTC.
-- ------------------------------------------------------------------------------
create or replace function public.reset_daily_extraction_quotas()
returns void as $$
begin
    update public.profiles
    set extractions_today = 0,
        last_extraction_reset = now(),
        updated_at = now();
end;
$$ language plpgsql security definer;

-- ------------------------------------------------------------------------------
-- TRIGGER: Auto-create public.profiles record when new user signs up in auth.users
-- ------------------------------------------------------------------------------
create or replace function public.handle_new_user()
returns trigger as $$
begin
    insert into public.profiles (id, email, full_name, avatar_url)
    values (
        new.id,
        new.email,
        new.raw_user_meta_data->>'full_name',
        new.raw_user_meta_data->>'avatar_url'
    );
    return new;
end;
$$ language plpgsql security definer;

-- Drop trigger if already exists and recreate
drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created
    after insert on auth.users
    for each row execute procedure public.handle_new_user();

-- ==============================================================================
-- ROW LEVEL SECURITY (RLS) POLICIES (UPA-102)
-- Protects user data and prevents cross-tenant data leakage.
-- ==============================================================================
alter table public.profiles enable row level security;
alter table public.extractions enable row level security;
alter table public.affiliate_clicks enable row level security;

-- PROFILES POLICIES
create policy "Users can view their own profile"
    on public.profiles for select
    using (auth.uid() = id);

create policy "Users can update their own profile"
    on public.profiles for update
    using (auth.uid() = id);

-- EXTRACTIONS POLICIES
create policy "Users can view their own extractions or public extractions"
    on public.extractions for select
    using (auth.uid() = user_id or is_public = true);

create policy "Users can insert their own extractions"
    on public.extractions for insert
    with check (auth.uid() = user_id or auth.uid() is null);

create policy "Users can update their own extractions"
    on public.extractions for update
    using (auth.uid() = user_id);

create policy "Users can delete their own extractions"
    on public.extractions for delete
    using (auth.uid() = user_id);

-- AFFILIATE CLICKS POLICIES
create policy "Anyone can insert affiliate click telemetry"
    on public.affiliate_clicks for insert
    with check (true);

create policy "Users can view their own click history"
    on public.affiliate_clicks for select
    using (auth.uid() = user_id);
