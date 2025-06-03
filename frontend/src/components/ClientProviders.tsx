'use client';

import React, { useState, useEffect } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { AuthProvider } from '@/src/contexts/AuthContext';
import Navbar from '@/src/components/navbar/Navbar';
import axios from 'axios'

const ClientProviders = ({ children }: { children: React.ReactNode }) => {
  const [queryClient] = useState(() => new QueryClient());

  useEffect(() => {
    axios.get('http://localhost:8000/api/v1/auth/csrf/', {
      withCredentials: true,
    })
      .then(() => console.log('✅ CSRF cookie set by Django'))
      .catch(() => console.warn('❌ CSRF cookie failed to set'));
  }, []);

  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <Navbar />
        {children}
      </AuthProvider>
    </QueryClientProvider>
  );
};

export default ClientProviders;
