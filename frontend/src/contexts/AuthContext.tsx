'use client';

import React, { createContext, useContext } from 'react';
import {
  useQuery,
  QueryObserverResult,
  useQueryClient,
} from '@tanstack/react-query';
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

// 2. Define Context interface
interface AuthContextType {
  isAuthenticated: boolean;
  profile: UserProfile | null;
  loading: boolean;
  logout: () => Promise<void>;
  refreshProfile: () => Promise<QueryObserverResult<UserProfile, Error>>;
}

// 3. Create initial Context values and attach types/interface
const AuthContext = createContext<AuthContextType>({
  isAuthenticated: false,
  profile: null,
  loading: true,
  logout: async () => { },
  refreshProfile: async () => {
    throw new Error('refreshProfile not implemented');
  },
});

function getCookie(name: string): string | null {
  const match = document.cookie.match(new RegExp(`(^| )${name}=([^;]+)`));
  return match ? match[2] : null;
}

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const {
    data: profile,
    isLoading,
    isError,
    refetch,
  } = useQuery<UserProfile>({
    queryKey: ['profile'],
    queryFn: async () => {
      const response = await axios.get(
        'http://localhost:8000/api/v1/accounts/profile/',
        {
          withCredentials: true,
        }
      );
      return response.data;
    },
    retry: false,
  });

  const queryClient = useQueryClient();
  // 5. Logout function that tells backend and clears profile
  const logout = async () => {
    const csrfToken = getCookie('csrftoken');

    if (!csrfToken) {
      console.error('CSRF token not found. Logout aborted.');
      return;
    }


    try {
      const logoutResponse = await axios.post(
        'http://localhost:8000/api/v1/auth/logout/',
        {},
        {
          withCredentials: true,
          headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json',
          },
        }
      );

      queryClient.removeQueries({ queryKey: ['profile'], exact: true });

      await refetch();
    } catch (error) {
      console.error('Logout error:', error);
    }
  };

  // 6. Provide everything to your app through context
  return (
    <AuthContext.Provider
      value={{
        isAuthenticated: !!profile && !isError,
        // The reason we use !! is to make sure that the profile returns a boolean and not data
        profile: profile || null,
        loading: isLoading,
        logout,
        refreshProfile: refetch,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

// 7. Custom hook so you can use auth data anywhere in your app
export const useAuth = () => useContext(AuthContext);
