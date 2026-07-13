alter table public.follow_up_tasks
  add column if not exists assigned_role public.portal_role not null default 'clinician',
  add column if not exists domain text,
  add column if not exists priority text,
  add column if not exists due_window text,
  add column if not exists source text not null default 'generated-follow-up-plan';

create index if not exists follow_up_assessment_idx
  on public.follow_up_tasks(assessment_id, due_date);

create index if not exists follow_up_domain_priority_idx
  on public.follow_up_tasks(owner_id, domain, priority, status);
