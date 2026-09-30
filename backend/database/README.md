# 🗄️ Universal Pro AI — Database Deployment Guide

This directory contains the database migration scripts for **Universal Pro AI** hosted on **Supabase** (PostgreSQL 15+).

---

## 📁 Migration Files

| Migration | File | Epics Covered | Description |
| :--- | :--- | :--- | :--- |
| **001** | `001_initial_schema.sql` | `UPA-101`, `UPA-102`, `UPA-103` | Tables (`profiles`, `extractions`, `affiliate_clicks`), RLS security policies, SHA-256 URL hash index, and automatic user profile triggers. |

---

## 🚀 How to Apply to Supabase (3 Simple Steps)

### Step 1: Create a Free Project on Supabase
1. Go to [supabase.com](https://supabase.com) and sign in.
2. Click **New Project**.
3. Set:
   - **Project Name**: `universal-pro-ai`
   - **Database Password**: *(Save securely)*
   - **Region**: Choose closest to target audience (e.g. `South Asia (Mumbai)` or `AWS Singapore`).
4. Click **Create new project** (takes ~60 seconds to provision).

### Step 2: Run the Initial Migration Script
1. In the Supabase Dashboard left sidebar, click the **SQL Editor** icon (looks like `>_`).
2. Click **New query**.
3. Copy the full contents of `database/001_initial_schema.sql` and paste it into the editor.
4. Click the green **Run** button (bottom right) or press `Ctrl + Enter`.
5. You should see: `Success. No rows returned`.

### Step 3: Copy Your API Keys to Environment
In Supabase:
1. Go to **Project Settings** (gear icon) $\rightarrow$ **API**.
2. Copy:
   - **Project URL**: (e.g., `https://xyzcompany.supabase.co`)
   - **anon / public key**: (used by frontend)
   - **service_role key**: (used securely by FastAPI backend & Celery workers)
3. Add these to your `.env` file:
   ```env
   SUPABASE_URL=https://your-project-id.supabase.co
   SUPABASE_ANON_KEY=your-anon-key-here
   SUPABASE_SERVICE_ROLE_KEY=your-service-role-key-here
   ```

---

## 🛡️ Security Features Implemented
- **Row Level Security (RLS)**: Users can only read, update, or delete extractions that belong to their `auth.uid()`.
- **Public Share Links**: Extractions marked `is_public = true` can be read anonymously for viral sharing.
- **SHA-256 URL Caching**: Avoids re-processing identical social links, saving API costs and delivering instant sub-second responses.
