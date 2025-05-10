import type { Metadata } from 'next';
import './globals.css';
import ClientProviders from '@/src/components/ClientProviders';
export const metadata: Metadata = {
  title: 'HHS - Lost and Found',
  description: 'Lost and Found App',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <ClientProviders>
          {children}
        </ClientProviders>
      </body>
    </html>
  );
}
