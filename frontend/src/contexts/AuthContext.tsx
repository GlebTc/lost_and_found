'use client';

import React, { createContext, useContext } from 'react';
import { useQuery, QueryObserverResult } from '@tanstack/react-query';
import axios from 'axios';

// 1. Define profile interface
interface UserProfile {
  id: string;
  email: string;
  role: string;
  first_name?: string | null;
  last_name?: string | null;
  avatar_url?: string | null;
}

// 2. Define Context variable types
interface AuthContextType {
  isAuthenticated: boolean;
  profile: UserProfile | null;
  loading: boolean;
  logout: () => Promise<void>;
  refreshProfile: () => Promise<QueryObserverResult<UserProfile, Error>>;
}

// 3. Create the context with default values (used only for typing)
const AuthContext = createContext<AuthContextType>({
  isAuthenticated: false,
  profile: null,
  loading: true,
  logout: async () => {},
  refreshProfile: async () => {
    throw new Error('refreshProfile not implemented');
  },
});

// 4. Provide the context using React Query for live profile fetching
export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  // useQuery fetches profile from backend and keeps it in sync
  const {
    data: profile,         // profile returned from backend
    isLoading,             // true while loading
    isError,               // true if error occurs (e.g., not logged in)
    refetch,               // function to manually re-fetch profile
  } = useQuery<UserProfile>({
    queryKey: ['profile'],
    queryFn: async () => {
      const response = await axios.get('http://localhost:8000/api/v1/accounts/profile/', {
        withCredentials: true,
      });
      return response.data;
    },
    retry: false, // don’t retry failed requests automatically
  });

  // 5. Logout function that tells backend and clears profile
  const logout = async () => {
    try {
      await axios.post('http://localhost:8000/api/v1/auth/logout/', {}, {
        withCredentials: true,
      });
      
      await refetch(); // after logout, re-fetch profile (should fail and clear context)
    } catch (error) {
      console.error('Logout error:', error);
    }
  };

  // 6. Provide everything to your app through context
  return (
    <AuthContext.Provider
      value={{
        isAuthenticated: !!profile && !isError,
        profile: profile || null,
        loading: isLoading,
        logout,
        refreshProfile: refetch, // full access to re-fetch result
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

// 7. Custom hook so you can use auth data anywhere in your app
export const useAuth = () => useContext(AuthContext);
