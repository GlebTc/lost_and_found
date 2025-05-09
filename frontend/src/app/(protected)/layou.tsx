// app/(protected)/layout.tsx
'use client';

import { useAuth } from '@/src/contexts/AuthContext';
import Loading from '@/src/components/reusable/Loading';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';

const ProtectedLayout = ({ children }: { children: React.ReactNode }) => {
  const { isAuthenticated, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && !isAuthenticated) {
      router.push('/login'); // redirect to login if not authenticated
    }
  }, [loading, isAuthenticated, router]);

  if (loading) return <Loading message="Checking authentication..." />;
  if (!isAuthenticated) return null;

  return <>{children}</>;
};

export default ProtectedLayout;
