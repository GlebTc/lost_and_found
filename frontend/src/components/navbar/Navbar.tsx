'use client';
import { useState } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import hhs_logo from '@/public/images/logo/hhs_logo.webp';
import { useAuth } from '@/src/contexts/AuthContext';
import AvatarDropdown from './AvatarDropdown';

const Navbar = () => {
  const componentName = 'NAVBAR';
  const { isAuthenticated, profile, logout } = useAuth();
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <nav className='bg-gray-100 fixed w-full h-[var(--navbar-h)] flex justify-between items-center px-4 md:px-20 border-b-1 border-gray-500'>
      <Link
        href='/'
        className='flex items-center gap-2 rounded-xl'
      >
        <Image
          src={hhs_logo}
          alt='Hamilton Health Sciences'
          width={40}
          height={40}
          className='h-10 w-auto rounded-xl'
        />
      </Link>

      <div
        className={`${componentName}_CONTENT_CONTAINER w-fit flex items-center justify-end gap-8`}
      >
        {/* Avatar and Dropdown */}
        {isAuthenticated && (
          <div className='AVATAR_CONTAINER relative'>
            <div
              onClick={() => setMenuOpen((prev) => !prev)}
              className='cursor-pointer'
            >
              {profile?.avatar_url ? (
                <img
                  src={profile.avatar_url}
                  alt='User Avatar'
                  className='w-14 h-14 rounded-full object-cover border border-gray-400'
                />
              ) : (
                <div className='w-10 h-10 rounded-full bg-cyan-700 hover:bg-cyan-600 text-white flex items-center justify-center text-xl font-bold transition duration-[var(--duration)]'>
                  {profile?.first_name
                    ? profile.first_name[0].toUpperCase()
                    : profile?.email[0].toUpperCase()}
                </div>
              )}
            </div>
            <AvatarDropdown menuOpen={menuOpen} />
          </div>
        )}

        {/* Login/Logout Button */}
        {isAuthenticated ? (
          <button
            onClick={logout}
            className='text-[var(--main-color)] border-1 border-[var(--main-color)] px-4 py-2 rounded-md hover:bg-gray-300 cursor-pointer duration-[var(--duration)]'
          >
            Log Out
          </button>
        ) : (
          <Link
            href='/login'
            className='text-[var(--main-color)] border-1 border-[var(--main-color)] px-4 py-2 rounded-md hover:bg-gray-300 cursor-pointer duration-[var(--duration)]'
          >
            Log In
          </Link>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
