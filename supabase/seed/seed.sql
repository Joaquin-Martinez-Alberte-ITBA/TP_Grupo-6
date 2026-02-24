insert into sites(id,name) values ('site-central','Hospital Central') on conflict do nothing;

insert into departments(site_id,name) values
('site-central','Clínica Médica'),
('site-central','Ginecología'),
('site-central','Pediatría')
on conflict do nothing;

-- crear usuarios en Supabase Auth manualmente y luego actualizar auth_user_id
-- ejemplo:
-- update doctors set auth_user_id = 'uuid-del-auth-user' where name = 'Dra. Ana Pérez';

insert into doctors(site_id,department_id,name)
select 'site-central', d.id, x.name
from (values
('Clínica Médica', 'Dr. Juan López'),
('Ginecología', 'Dra. Ana Pérez'),
('Pediatría', 'Dr. Carlos Díaz')
) as x(dep_name, name)
join departments d on d.name = x.dep_name and d.site_id = 'site-central'
on conflict do nothing;
