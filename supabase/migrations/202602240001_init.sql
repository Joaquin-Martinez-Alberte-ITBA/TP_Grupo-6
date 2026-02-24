create extension if not exists pgcrypto;

create type ticket_status as enum ('WAITING','CALLED','IN_CONSULT','DONE');

create table if not exists sites (
  id text primary key,
  name text not null
);

create table if not exists departments (
  id uuid primary key default gen_random_uuid(),
  site_id text not null references sites(id) on delete cascade,
  name text not null
);

create table if not exists doctors (
  id uuid primary key default gen_random_uuid(),
  site_id text not null references sites(id) on delete cascade,
  department_id uuid not null references departments(id) on delete cascade,
  name text not null,
  auth_user_id uuid unique
);

create table if not exists tickets (
  id uuid primary key default gen_random_uuid(),
  site_id text not null references sites(id) on delete cascade,
  department_id uuid not null references departments(id),
  doctor_id uuid references doctors(id),
  ticket_number text not null,
  status ticket_status not null default 'WAITING',
  reason_category text not null,
  reason_text text,
  patient_name text,
  patient_id_number text,
  patient_dob date,
  patient_phone text,
  insurance text,
  public_token text not null unique,
  created_at timestamptz not null default now(),
  called_at timestamptz,
  completed_at timestamptz
);

create index if not exists idx_tickets_site_created on tickets(site_id, created_at);
create index if not exists idx_tickets_status on tickets(status);

create or replace function create_ticket(
  p_site_id text,
  p_department_id uuid,
  p_reason_category text,
  p_reason_text text,
  p_patient_name text,
  p_patient_id_number text,
  p_patient_dob date,
  p_patient_phone text,
  p_public_token text
)
returns json
language plpgsql
security definer
as $$
declare
  v_count int;
  v_ticket_number text;
  v_id uuid;
begin
  select count(*) into v_count
  from tickets
  where site_id = p_site_id and created_at::date = now()::date;

  v_ticket_number := 'A-' || (v_count + 1)::text;

  insert into tickets(
    site_id, department_id, ticket_number, reason_category, reason_text,
    patient_name, patient_id_number, patient_dob, patient_phone, public_token
  ) values (
    p_site_id, p_department_id, v_ticket_number, p_reason_category, p_reason_text,
    p_patient_name, p_patient_id_number, p_patient_dob, p_patient_phone, p_public_token
  ) returning id into v_id;

  return json_build_object('id', v_id, 'ticket_number', v_ticket_number, 'public_token', p_public_token);
end;
$$;

create or replace function doctor_call_next(p_doctor_id uuid)
returns json
language plpgsql
security definer
as $$
declare
  v_department uuid;
  v_ticket_id uuid;
  v_ticket_number text;
begin
  select department_id into v_department from doctors where id = p_doctor_id;
  if v_department is null then
    raise exception 'Doctor inválido';
  end if;

  select id, ticket_number into v_ticket_id, v_ticket_number
  from tickets
  where department_id = v_department and status = 'WAITING'
  order by created_at asc
  limit 1
  for update skip locked;

  if v_ticket_id is null then
    return json_build_object('message', 'Sin tickets en espera');
  end if;

  update tickets
  set status = 'CALLED', doctor_id = p_doctor_id, called_at = now()
  where id = v_ticket_id;

  return json_build_object('id', v_ticket_id, 'ticket_number', v_ticket_number);
end;
$$;

alter table doctors enable row level security;
alter table tickets enable row level security;

create policy "doctor can read own profile" on doctors
for select to authenticated
using (auth.uid() = auth_user_id);

create policy "doctor can read dept tickets" on tickets
for select to authenticated
using (exists (
  select 1 from doctors d
  where d.auth_user_id = auth.uid() and d.department_id = tickets.department_id
));

create policy "doctor can update dept tickets" on tickets
for update to authenticated
using (exists (
  select 1 from doctors d
  where d.auth_user_id = auth.uid() and d.department_id = tickets.department_id
));

revoke all on function create_ticket(text,uuid,text,text,text,text,date,text,text) from public;
revoke all on function doctor_call_next(uuid) from public;
grant execute on function doctor_call_next(uuid) to authenticated;
grant execute on function create_ticket(text,uuid,text,text,text,text,date,text,text) to service_role;
