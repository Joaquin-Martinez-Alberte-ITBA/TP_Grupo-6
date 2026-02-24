'use client';

import { useEffect, useState } from 'react';

type Ticket = {
  id: string;
  ticket_number: string;
  status: string;
  reason_category: string;
  department_name: string;
};

export default function TicketStatus({ ticketId, token }: { ticketId: string; token: string }) {
  const [ticket, setTicket] = useState<Ticket | null>(null);
  const [error, setError] = useState('');

  useEffect(() => {
    let stop = false;
    async function load() {
      const res = await fetch(`/api/tickets/${ticketId}?token=${token}`);
      const data = await res.json();
      if (!res.ok) {
        setError(data.error ?? 'No autorizado');
        return;
      }
      if (!stop) setTicket(data);
    }
    load();
    const id = setInterval(load, 2000);
    return () => {
      stop = true;
      clearInterval(id);
    };
  }, [ticketId, token]);

  if (error) return <div className="card"><p>{error}</p></div>;
  if (!ticket) return <div className="card"><p>Cargando ticket...</p></div>;

  return (
    <div className="card">
      <h1>Tu ticket</h1>
      <p className="pill">#{ticket.ticket_number}</p>
      <p>Estado: <strong>{ticket.status}</strong></p>
      <p>Sector: {ticket.department_name}</p>
      <p>Te avisaremos cuando sea tu turno.</p>
    </div>
  );
}
