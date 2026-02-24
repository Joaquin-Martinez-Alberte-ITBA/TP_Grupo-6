'use client';

import { useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';

const categories = [
  { value: 'clinica', label: 'Clínica' },
  { value: 'gineco', label: 'Ginecología' },
  { value: 'pediatria', label: 'Pediatría' },
  { value: 'urologia', label: 'Urología' },
  { value: 'traumatologia', label: 'Traumatología' }
];

export default function CheckinForm() {
  const router = useRouter();
  const search = useSearchParams();
  const site = search.get('site') ?? '';
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  async function onSubmit(formData: FormData) {
    setLoading(true);
    setError('');
    const payload = Object.fromEntries(formData.entries());
    const res = await fetch('/api/tickets', {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ ...payload, site_id: site })
    });
    const data = await res.json();
    if (!res.ok) {
      setError(data.error ?? 'No se pudo generar el ticket');
      setLoading(false);
      return;
    }
    localStorage.setItem('patient_ticket', JSON.stringify({ id: data.id, token: data.public_token }));
    router.push(`/ticket/${data.id}?token=${data.public_token}`);
  }

  return (
    <form action={onSubmit} className="card">
      <h1>Check-in de paciente</h1>
      <p>Site: <strong>{site || 'No especificado'}</strong></p>
      <label>Nombre y apellido<input required name="patient_name" /></label>
      <label>DNI/ID<input name="patient_id_number" /></label>
      <label>Fecha de nacimiento<input required type="date" name="patient_dob" /></label>
      <label>Teléfono<input name="patient_phone" /></label>
      <label>Obra social<input name="insurance" /></label>
      <label>Categoría
        <select name="reason_category" defaultValue="clinica">
          {categories.map((c) => <option key={c.value} value={c.value}>{c.label}</option>)}
        </select>
      </label>
      <label>Motivo de consulta<textarea name="reason_text" rows={4} /></label>
      {error && <p style={{ color: 'crimson' }}>{error}</p>}
      <button disabled={loading}>{loading ? 'Generando...' : 'Generar ticket'}</button>
    </form>
  );
}
