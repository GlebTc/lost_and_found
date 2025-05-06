'use client';

import React from 'react';
import { useAuth } from '@/src/contexts/AuthContext';

const Main = () => {
  const { isAuthenticated, profile, loading } = useAuth();

  if (loading) {
    return <div className="text-center mt-10 text-gray-500">Checking authentication...</div>;
  }

  return (
    <div className="p-6 text-gray-900 dark:text-gray-100">
      <h1 className="text-2xl font-bold mb-4">Main Page</h1>

      {isAuthenticated && profile ? (
        <div className="bg-gray-100 dark:bg-gray-800 p-4 rounded-lg shadow">
          <p><strong>Welcome, {profile.first_name || profile.email}!</strong></p>
          <p>Email: {profile.email}</p>
          <p>Role: {profile.role}</p>
          {profile.avatar_url && (
            <img src={profile.avatar_url} alt="User avatar" className="mt-2 rounded-full w-20 h-20 object-cover" />
          )}
        </div>
      ) : (
        <p>You are not logged in.</p>
      )}
    </div>
  );
};

export default Main;
