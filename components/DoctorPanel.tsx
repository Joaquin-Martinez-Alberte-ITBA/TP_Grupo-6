'use client';

import { useEffect, useState } from 'react';
import { supabaseBrowser } from '@/lib/supabase-browser';

type Ticket = {
  id: string;
  ticket_number: string;
  status: string;
  reason_category: string;
  patient_name: string;
  department_name: string;
};

export default function DoctorPanel() {
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [session, setSession] = useState(false);

  async function authHeader() {
    const { data } = await supabaseBrowser.auth.getSession();
    const token = data.session?.access_token;
    return token ? { Authorization: `Bearer ${token}` } : {};
  }

  async function loadTickets() {
    const headers = await authHeader();
    const res = await fetch('/api/doctor/tickets', { headers });
    if (!res.ok) return;
    setTickets(await res.json());
  }

  useEffect(() => {
    supabaseBrowser.auth.getSession().then(({ data }) => setSession(Boolean(data.session)));
    const { data: listener } = supabaseBrowser.auth.onAuthStateChange((_e, sessionData) => setSession(Boolean(sessionData)));
    return () => listener.subscription.unsubscribe();
  }, []);

  useEffect(() => {
    if (!session) return;
    loadTickets();
    const channel = supabaseBrowser.channel('doctor-queue').on('postgres_changes', {
      event: '*', schema: 'public', table: 'tickets'
    }, () => loadTickets()).subscribe();

    return () => { supabaseBrowser.removeChannel(channel); };
  }, [session]);

  async function login() {
    await supabaseBrowser.auth.signInWithPassword({ email, password });
  }

  async function changeStatus(ticketId: string, status: string) {
    const headers = { 'Content-Type': 'application/json', ...(await authHeader()) };
    await fetch(`/api/doctor/tickets/${ticketId}/status`, { method: 'PATCH', headers, body: JSON.stringify({ status }) });
    loadTickets();
  }

  async function callNext() {
    const headers = await authHeader();
    await fetch('/api/doctor/call-next', { method: 'POST', headers });
    loadTickets();
  }

  if (!session) {
    return (
      <div className="card">
        <h1>Ingreso médico</h1>
        <label>Email<input value={email} onChange={(e) => setEmail(e.target.value)} /></label>
        <label>Contraseña<input type="password" value={password} onChange={(e) => setPassword(e.target.value)} /></label>
        <button type="button" onClick={login}>Iniciar sesión</button>
      </div>
    );
  }

  return (
    <div className="card">
      <h1>Panel médico</h1>
      <button type="button" onClick={callNext}>Llamar siguiente</button>
      <ul>
        {tickets.map((t) => (
          <li key={t.id} style={{ marginBottom: '.75rem' }}>
            <strong>{t.ticket_number}</strong> · {t.patient_name || 'Paciente'} · {t.department_name} · <em>{t.status}</em>
            <div className="row">
              <button type="button" className="secondary" onClick={() => changeStatus(t.id, 'IN_CONSULT')}>En consulta</button>
              <button type="button" className="secondary" onClick={() => changeStatus(t.id, 'DONE')}>Finalizar</button>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
