import { NextRequest, NextResponse } from 'next/server';
import { z } from 'zod';
import { getServiceSupabase } from '@/lib/supabase-server';
import { resolveDepartmentName } from '@/lib/routing';
import crypto from 'crypto';

const schema = z.object({
  site_id: z.string().min(1),
  reason_category: z.string(),
  reason_text: z.string().optional().nullable(),
  patient_name: z.string().optional().nullable(),
  patient_id_number: z.string().optional().nullable(),
  patient_dob: z.string().optional().nullable(),
  patient_phone: z.string().optional().nullable()
});

export async function POST(req: NextRequest) {
  try {
    const body = schema.parse(await req.json());
    const supabase = getServiceSupabase();
    const departmentName = resolveDepartmentName(body.reason_category);
    const { data: dept, error: deptErr } = await supabase
      .from('departments')
      .select('id')
      .eq('site_id', body.site_id)
      .eq('name', departmentName)
      .single();

    if (deptErr || !dept) return NextResponse.json({ error: 'Departamento no encontrado' }, { status: 400 });

    const public_token = crypto.randomBytes(16).toString('hex');
    const { data, error } = await supabase.rpc('create_ticket', {
      p_site_id: body.site_id,
      p_department_id: dept.id,
      p_reason_category: body.reason_category,
      p_reason_text: body.reason_text ?? null,
      p_patient_name: body.patient_name ?? null,
      p_patient_id_number: body.patient_id_number ?? null,
      p_patient_dob: body.patient_dob ?? null,
      p_patient_phone: body.patient_phone ?? null,
      p_public_token: public_token
    });

    if (error) return NextResponse.json({ error: error.message }, { status: 400 });
    return NextResponse.json(data);
  } catch {
    return NextResponse.json({ error: 'Payload inválido' }, { status: 400 });
  }
}
