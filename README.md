# NOMBRE_PROYECTO - MVP Check-in Hospitalario por QR

MVP de check-in hospitalario mobile-first con cola de turnos para médicos.

## Stack
- Next.js 14 (App Router) + TypeScript
- Supabase (Postgres, Auth, Realtime, RLS)
- UI minimalista en español

## Funcionalidades incluidas
- `/checkin?site=site-central`: formulario de ingreso paciente (anónimo).
- Routing por reglas simples `categoría -> departamento`.
- Generación de ticket incremental por sitio y día (`A-1`, `A-2`, ...).
- Vista de ticket del paciente: `/ticket/:ticketId?token=:public_token`.
- `/doctor`: login de médicos (Supabase Auth) y gestión de cola.
- Acciones médicas: llamar siguiente, en consulta, finalizar.
- Actualización en tiempo real para panel médico con Supabase Realtime.
- RLS para que médicos solo vean tickets de su departamento.

## Estructura
- `app/`: páginas y API routes de Next.js.
- `components/`: UI de check-in, ticket y doctor.
- `lib/`: clientes Supabase, routing y utilidades.
- `supabase/migrations/`: esquema SQL + RLS + funciones.
- `supabase/seed/seed.sql`: datos iniciales.
- `scripts/generate-qr.mjs`: genera un PNG QR para la URL de check-in.

## Prerrequisitos
- Node.js 20+
- npm 10+
- Supabase CLI (`npm i -g supabase`)
- Docker (para Supabase local)

## 1) Instalar dependencias
```bash
npm install
```

## 2) Levantar Supabase local
```bash
supabase start
```

Obtener claves locales:
```bash
supabase status
```

## 3) Configurar variables de entorno
```bash
cp .env.example .env.local
```

Completar `NEXT_PUBLIC_SUPABASE_ANON_KEY` y `SUPABASE_SERVICE_ROLE_KEY` con los valores de `supabase status`.

## 4) Aplicar migraciones y seed
```bash
supabase db reset
psql postgresql://postgres:postgres@127.0.0.1:54322/postgres -f supabase/seed/seed.sql
```

## 5) Crear usuarios médicos en Auth y vincularlos
Crear usuarios en Supabase Studio (Authentication > Users), por ejemplo:
- doctor1@hospital.local / 12345678
- doctor2@hospital.local / 12345678
- doctor3@hospital.local / 12345678

Luego vincular:
```sql
update doctors set auth_user_id = '<UUID_USER_1>' where name = 'Dr. Juan López';
update doctors set auth_user_id = '<UUID_USER_2>' where name = 'Dra. Ana Pérez';
update doctors set auth_user_id = '<UUID_USER_3>' where name = 'Dr. Carlos Díaz';
```

## 6) Correr la app
```bash
npm run dev
```
Abrir: `http://localhost:3000`

## 7) Generar QR del check-in
```bash
npm run gen:qr -- "http://localhost:3000/checkin?site=site-central" "public/checkin-qr.png"
```

## Flujo de prueba rápido
1. Paciente abre `/checkin?site=site-central`.
2. Completa formulario y obtiene ticket.
3. Médico entra a `/doctor`, inicia sesión y pulsa **Llamar siguiente**.
4. El estado cambia en el paciente (polling corto de 2s) y en panel médico en realtime.

## Decisiones técnicas
- **Privacidad QR**: solo contiene URL con `site` (sin datos personales).
- **Acceso paciente a ticket**: mediante `ticketId + public_token`.
- **RLS médico**: lectura/actualización restringida por `department_id` asignado.
- **Creación de ticket**: función SQL `create_ticket` para número incremental diario.
- **Escalabilidad**: separación clara entre UI, API, lógica de routing y SQL.

## Extensión futura
- Habilitar routing inteligente (LLM) usando el hook `llmRoutingHookDisabled()`.
- Realtime también para paciente con canal autenticado por token corto.
- Transferencia entre departamentos desde panel médico.
- Auditoría y métricas de tiempos por ticket.
