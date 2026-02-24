import { NextRequest, NextResponse } from 'next/server';
import { getUserClient } from '@/lib/server-auth';

async function getDoctorId(client: ReturnType<typeof getUserClient>) {
  if (!client) return null;
  const { data: userData } = await client.auth.getUser();
  if (!userData.user) return null;
  const { data } = await client.from('doctors').select('id').eq('auth_user_id', userData.user.id).single();
  return data?.id ?? null;
}

export async function GET(req: NextRequest) {
  const client = getUserClient(req.headers.get('authorization'));
  const doctorId = await getDoctorId(client);
  if (!doctorId || !client) return NextResponse.json({ error: 'No autorizado' }, { status: 401 });

  const { data, error } = await client
    .from('tickets')
    .select('id,ticket_number,status,reason_category,patient_name,departments(name)')
    .in('status', ['WAITING', 'CALLED', 'IN_CONSULT'])
    .order('created_at', { ascending: true });

  if (error) return NextResponse.json({ error: error.message }, { status: 400 });
  const rows = (data ?? []).map((t) => ({ ...t, department_name: (t.departments as { name: string } | null)?.name ?? '-' }));
  return NextResponse.json(rows);
}
