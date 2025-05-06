'use client';

import React, { createContext, useContext, useEffect, useState } from 'react';
import axios from 'axios';

// Types for user Profile - this is consistent with the Profile model in Django
interface UserProfile {
  id: string;                 
  email: string;              
  role: string;               
  first_name?: string | null; 
  last_name?: string | null;  
  avatar_url?: string | null; 
}

// Types for functions and values of the auth context
interface AuthContextType {
  isAuthenticated: boolean;         
  profile: UserProfile | null;      
  loading: boolean;                 
  logout: () => void;               
  refreshProfile: () => Promise<void>; // ✅ Now available for components to use
}

// Inittiate auth context with default values that will be modified/used in the app
const AuthContext = createContext<AuthContextType>({
  isAuthenticated: false,
  profile: null,
  loading: true,
  logout: () => {},
  refreshProfile: async () => {},
});

// Create a AuthProvider component
export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(true);

  // ✅ Reusable function to fetch profile data
  const refreshProfile = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/v1/accounts/profile/', {
        withCredentials: true,
      });
      setProfile(response.data);
    } catch (error) {
      console.error("Error refreshing profile:", error);
      setProfile(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    refreshProfile();
  }, []);

  const logout = async () => {
    try {
      await axios.post('http://localhost:8000/api/v1/auth/logout/', {}, {
        withCredentials: true,
      });
      setProfile(null);
    } catch (error) {
      console.error('Logout failed', error);
    }
  };

  return (
    <AuthContext.Provider value={{ isAuthenticated: !!profile, profile, loading, logout, refreshProfile }}>
      {children}
    </AuthContext.Provider>
  );
};

// 🪝 Hook to use the auth context anywhere in your app
export const useAuth = () => useContext(AuthContext);
