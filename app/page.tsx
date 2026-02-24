import Link from 'next/link';

export default function Home() {
  return (
    <main>
      <div className="card">
        <h1>Hospital Check-in MVP</h1>
        <p>Ingreso por QR para pacientes y cola en tiempo real para médicos.</p>
        <ul>
          <li><Link href="/checkin?site=site-central">Ir a check-in (demo)</Link></li>
          <li><Link href="/doctor">Panel médico</Link></li>
        </ul>
      </div>
    </main>
  );
}
