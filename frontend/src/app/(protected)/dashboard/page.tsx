'use client';

import { useAuth } from '@/src/contexts/AuthContext';
import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import DashboardHero from './DashboardHero';

const DashboardMain = () => {
  const { isAuthenticated } = useAuth();
  const router = useRouter();

  // If not authenticated, redirect to login page
  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login');
    }
  }, [isAuthenticated, router]);

  // Optional: render nothing while checking
  if (!isAuthenticated) return null;

  return (
    <div className='p-8 text-gray-800 pt-[var(--navbar-h)] bg-gray-200 min-h-screen'>
      <DashboardHero />
    </div>
  );
};

export default DashboardMain;
