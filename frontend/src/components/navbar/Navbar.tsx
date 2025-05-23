'use client';
import { useEffect, useRef, useState } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import hhs_logo from '@/public/images/logo/hhs_logo.webp';
import { useAuth } from '@/src/contexts/AuthContext';
import AvatarDropdown from './AvatarDropdown';

const Navbar = () => {
  const componentName = 'NAVBAR';
  const { isAuthenticated, profile, logout } = useAuth();
  const [menuOpen, setMenuOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        dropdownRef.current &&
        !dropdownRef.current.contains(event.target as Node)
      ) {
        setMenuOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  return (
    <nav className='bg-gray-100 fixed w-full h-[var(--navbar-h)] flex justify-between items-center px-4 md:px-20 border-b-1 border-gray-500'>
      <Link href='/' className='flex items-center gap-2 rounded-xl'>
        <Image
          src={hhs_logo}
          alt='Hamilton Health Sciences'
          width={40}
          height={40}
          className='h-10 w-auto rounded-xl'
        />
      </Link>

      <div className={`${componentName}_CONTENT_CONTAINER w-fit flex items-center justify-end gap-8`}>
        {isAuthenticated && (
          <div className='AVATAR_CONTAINER relative' ref={dropdownRef}>
            <div onClick={() => setMenuOpen((prev) => !prev)} className='cursor-pointer'>
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
            <AvatarDropdown menuOpen={menuOpen} setMenuOpen={setMenuOpen} />
          </div>
        )}

        {!isAuthenticated && (
          <Link href='/login' className='button_main'>
            Log In
          </Link>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
