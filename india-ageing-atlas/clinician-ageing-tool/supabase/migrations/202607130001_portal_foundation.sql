create extension if not exists pgcrypto;

create type public.portal_role as enum ('clinician', 'patient', 'caregiver', 'researcher', 'admin');
create type public.task_status as enum ('planned', 'in_progress', 'done', 'deferred');

create table public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  display_name text,
  role public.portal_role not null default 'patient',
  preferred_language text not null default 'en',
  organisation text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  constraint preferred_language_supported check (preferred_language in ('en', 'hi', 'kn', 'ta', 'te', 'mr'))
);

create table public.consent_events (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  consent_version text not null,
  accepted boolean not null,
  purpose text not null,
  language_code text not null default 'en',
  ip_context inet,
  user_agent text,
  created_at timestamptz not null default now()
);

create table public.assessments (
  id uuid primary key default gen_random_uuid(),
  owner_id uuid not null references auth.users(id) on delete cascade,
  patient_code text,
  role_context public.portal_role not null default 'clinician',
  language_code text not null default 'en',
  patient_snapshot jsonb not null default '{}'::jsonb,
  spirometry_result jsonb not null default '{}'::jsonb,
  care_map jsonb not null default '[]'::jsonb,
  clinician_actions jsonb not null default '[]'::jsonb,
  patient_plan jsonb not null default '[]'::jsonb,
  follow_up_plan jsonb not null default '{}'::jsonb,
  consent_context jsonb not null default '{}'::jsonb,
  report_text text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  constraint assessment_language_supported check (language_code in ('en', 'hi', 'kn', 'ta', 'te', 'mr'))
);

create table public.follow_up_tasks (
  id uuid primary key default gen_random_uuid(),
  assessment_id uuid not null references public.assessments(id) on delete cascade,
  owner_id uuid not null references auth.users(id) on delete cascade,
  title text not null,
  details text,
  due_date date,
  status public.task_status not null default 'planned',
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table public.education_modules (
  id uuid primary key default gen_random_uuid(),
  slug text not null,
  language_code text not null,
  role_context public.portal_role not null default 'patient',
  title text not null,
  body text not null,
  clinical_boundary text not null default 'Education only; not a diagnosis, prescription, or emergency triage instruction.',
  source_note text,
  version text not null default 'v1',
  is_active boolean not null default true,
  created_at timestamptz not null default now(),
  unique (slug, language_code, role_context, version),
  constraint education_language_supported check (language_code in ('en', 'hi', 'kn', 'ta', 'te', 'mr'))
);

create index assessments_owner_created_idx on public.assessments(owner_id, created_at desc);
create index follow_up_owner_status_idx on public.follow_up_tasks(owner_id, status, due_date);
create index education_lookup_idx on public.education_modules(language_code, role_context, is_active);

alter table public.profiles enable row level security;
alter table public.consent_events enable row level security;
alter table public.assessments enable row level security;
alter table public.follow_up_tasks enable row level security;
alter table public.education_modules enable row level security;

create policy "profiles are visible to owner"
  on public.profiles for select
  using (auth.uid() = id);

create policy "profiles are editable by owner"
  on public.profiles for all
  using (auth.uid() = id)
  with check (auth.uid() = id);

create policy "consent events are visible to owner"
  on public.consent_events for select
  using (auth.uid() = user_id);

create policy "users can create own consent events"
  on public.consent_events for insert
  with check (auth.uid() = user_id);

create policy "assessments are visible to owner"
  on public.assessments for select
  using (auth.uid() = owner_id);

create policy "users can create own assessments"
  on public.assessments for insert
  with check (auth.uid() = owner_id);

create policy "users can update own assessments"
  on public.assessments for update
  using (auth.uid() = owner_id)
  with check (auth.uid() = owner_id);

create policy "users can delete own assessments"
  on public.assessments for delete
  using (auth.uid() = owner_id);

create policy "follow up tasks are visible to owner"
  on public.follow_up_tasks for select
  using (auth.uid() = owner_id);

create policy "users can manage own follow up tasks"
  on public.follow_up_tasks for all
  using (auth.uid() = owner_id)
  with check (auth.uid() = owner_id);

create policy "active education modules are public"
  on public.education_modules for select
  using (is_active);

create or replace function public.set_updated_at()
returns trigger
language plpgsql
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

create trigger profiles_set_updated_at
  before update on public.profiles
  for each row execute function public.set_updated_at();

create trigger assessments_set_updated_at
  before update on public.assessments
  for each row execute function public.set_updated_at();

create trigger follow_up_tasks_set_updated_at
  before update on public.follow_up_tasks
  for each row execute function public.set_updated_at();

create or replace function public.handle_new_user()
returns trigger
language plpgsql
security definer
set search_path = public
as $$
begin
  insert into public.profiles (id, display_name, role, preferred_language)
  values (
    new.id,
    coalesce(new.raw_user_meta_data->>'name', split_part(new.email, '@', 1)),
    case
      when new.raw_user_meta_data->>'role' in ('clinician', 'patient', 'caregiver', 'researcher', 'admin')
        then (new.raw_user_meta_data->>'role')::public.portal_role
      else 'patient'::public.portal_role
    end,
    coalesce(new.raw_user_meta_data->>'preferred_language', 'en')
  )
  on conflict (id) do nothing;
  return new;
end;
$$;

create trigger on_auth_user_created
  after insert on auth.users
  for each row execute function public.handle_new_user();
