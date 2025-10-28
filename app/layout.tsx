import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Farcaster Prediction Market',
  description: 'Bet on Farcaster user statistics',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
