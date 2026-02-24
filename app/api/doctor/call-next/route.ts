import { NextRequest, NextResponse } from 'next/server';
import { getUserClient } from '@/lib/server-auth';

export async function POST(req: NextRequest) {
  const client = getUserClient(req.headers.get('authorization'));
  if (!client) return NextResponse.json({ error: 'No autorizado' }, { status: 401 });

  const { data: userData } = await client.auth.getUser();
  if (!userData.user) return NextResponse.json({ error: 'No autorizado' }, { status: 401 });

  const { data: doctor } = await client.from('doctors').select('id').eq('auth_user_id', userData.user.id).single();
  if (!doctor) return NextResponse.json({ error: 'Doctor no encontrado' }, { status: 404 });

  const { data, error } = await client.rpc('doctor_call_next', { p_doctor_id: doctor.id });
  if (error) return NextResponse.json({ error: error.message }, { status: 400 });
  return NextResponse.json(data ?? {});
}
