import './globals.css';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Hospital Check-in MVP',
  description: 'Sistema de check-in hospitalario por QR + cola de turnos'
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="es">
      <body>{children}</body>
    </html>
  );
}
