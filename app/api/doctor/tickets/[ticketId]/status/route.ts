import { NextRequest, NextResponse } from 'next/server';
import { getUserClient } from '@/lib/server-auth';

export async function PATCH(req: NextRequest, { params }: { params: { ticketId: string } }) {
  const client = getUserClient(req.headers.get('authorization'));
  if (!client) return NextResponse.json({ error: 'No autorizado' }, { status: 401 });

  const { status } = await req.json() as { status: 'IN_CONSULT' | 'DONE' };
  const patch: Record<string, string> = { status };
  if (status === 'DONE') patch.completed_at = new Date().toISOString();
  const { error } = await client.from('tickets').update(patch).eq('id', params.ticketId);
  if (error) return NextResponse.json({ error: error.message }, { status: 400 });
  return NextResponse.json({ ok: true });
}
