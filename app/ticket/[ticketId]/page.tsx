import TicketStatus from '@/components/TicketStatus';

export default function TicketPage({ params, searchParams }: { params: { ticketId: string }, searchParams: { token?: string } }) {
  return (
    <main>
      <TicketStatus ticketId={params.ticketId} token={searchParams.token ?? ''} />
    </main>
  );
}
