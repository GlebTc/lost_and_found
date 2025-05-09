'use client';

import { useAuth } from '@/src/contexts/AuthContext';

const DashboardUserInformation = () => {
  const { profile } = useAuth();

  if (!profile) return null; // Don't render if no user is logged in

  return (
    <div className="max-w-6xl mx-auto mb-6 mt-12">
      <div className="bg-white dark:bg-gray-800 shadow-md rounded-xl p-6 flex flex-col sm:flex-row sm:items-center justify-between gap-4 border border-gray-300 dark:border-gray-700">
        <div>
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
            Welcome back, {profile.first_name || profile.email}!
          </h2>
          <p className="text-gray-600 dark:text-gray-400 text-sm">
            You're logged in as a <span className="font-medium text-cyan-700 dark:text-cyan-400">{profile.role}</span>
          </p>
        </div>

        {/* Avatar - optional */}
        {profile.avatar_url ? (
          <img
            src={profile.avatar_url}
            alt="User Avatar"
            className="w-14 h-14 rounded-full object-cover border border-gray-400"
          />
        ) : (
          <div className="w-14 h-14 rounded-full bg-cyan-700 text-white flex items-center justify-center text-xl font-bold">
            {profile.first_name ? profile.first_name[0].toUpperCase() : profile.email[0].toUpperCase()}
          </div>
        )}
      </div>
    </div>
  );
};

export default DashboardUserInformation;
