import { NextRequest, NextResponse } from 'next/server';
import { getServiceSupabase } from '@/lib/supabase-server';

export async function GET(req: NextRequest, { params }: { params: { ticketId: string } }) {
  const token = req.nextUrl.searchParams.get('token');
  if (!token) return NextResponse.json({ error: 'Token requerido' }, { status: 401 });

  const supabase = getServiceSupabase();
  const { data, error } = await supabase
    .from('tickets')
    .select('id,ticket_number,status,reason_category,departments(name)')
    .eq('id', params.ticketId)
    .eq('public_token', token)
    .single();

  if (error || !data) return NextResponse.json({ error: 'Ticket no encontrado' }, { status: 404 });
  return NextResponse.json({
    ...data,
    department_name: (data.departments as { name: string } | null)?.name ?? '-'
  });
}
