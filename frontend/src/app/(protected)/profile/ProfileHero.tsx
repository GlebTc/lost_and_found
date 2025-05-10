'use client';
import { useAuth } from '@/src/contexts/AuthContext';

const ProfileHero = () => {
  const { profile } = useAuth();

  return (
    <section className='bg-gradient-to-b from-[var(--background)] to-[var(--main-color)] py-16 md:py-24 rounded-xl mt-12'>
      <div className='max-w-6xl mx-auto px-4 md:px-6'>
        <div className='grid gap-6 lg:grid-cols-2 lg:gap-12 items-center'>
          <div className='space-y-6'>
            <div className='space-y-4'>
              <h1 className='text-3xl md:text-5xl font-bold tracking-tight text-[hsl(var(--secondary))]'>
                Welcome, {profile?.first_name}!
              </h1>
              <p className='text-gray-700 dark:text-gray-300 md:text-xl'>
                Here's your profile summary. Use the options below to manage your account and view activity.
              </p>

              <div className='space-y-2 text-gray-800 dark:text-gray-200'>
                <p><strong>Name:</strong> {profile?.first_name} {profile?.last_name}</p>
                <p><strong>Email:</strong> {profile?.email}</p>
                <p><strong>Role:</strong> {profile?.role}</p>
              </div>

              <div className='grid grid-cols-2 gap-3 pt-4'>
                <a href='/settings'>
                  <button className='w-full px-6 py-3 rounded-lg bg-cyan-700 hover:bg-cyan-600 text-white font-semibold cursor-pointer transition duration-[var(--duration)]'>
                    Edit Settings
                  </button>
                </a>
                <a href='/dashboard'>
                  <button className='w-full px-6 py-3 rounded-lg bg-none hover:bg-gray-200 text-[var(--main-color)] border border-[var(--main-color)] font-semibold cursor-pointer transition duration-[var(--duration)]'>
                    Back to Dashboard
                  </button>
                </a>
              </div>
            </div>
          </div>

          <div className='lg:ml-auto'>
            <div className='aspect-square w-64 h-64 overflow-hidden rounded-full bg-gray-200 dark:bg-gray-700 mx-auto'>
              {profile?.avatar_url ? (
                <img
                  src={profile.avatar_url}
                  alt='User Avatar'
                  className='object-cover w-full h-full'
                />
              ) : (
                <div className='w-full h-full flex items-center justify-center text-6xl font-bold text-white bg-cyan-700'>
                  {profile?.first_name?.[0] || profile?.email?.[0]}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default ProfileHero;
