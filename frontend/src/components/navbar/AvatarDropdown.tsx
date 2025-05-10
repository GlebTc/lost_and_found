'use client';

import React from 'react';
import Link from 'next/link';
import { useAuth } from '@/src/contexts/AuthContext';

const AvatarDropdown = ({ menuOpen }: { menuOpen: boolean }) => {
  const { logout } = useAuth();

  const menuItems = [
    { label: 'My Profile', href: '/profile' },
    { label: 'Settings', href: '/settings' },
  ];

  return (
    <div
      className={`
        absolute left-0 mt-2 w-48 rounded-md bg-white shadow-lg border border-gray-200 overflow-hidden transform transition-all origin-top duration-[var(--duration)] z-50
        ${menuOpen ? 'opacity-100 scale-y-100' : 'opacity-0 scale-y-0 pointer-events-none'}
      `}
    >
      {menuItems.map(({ label, href }) => (
        <Link
          key={label}
          href={href}
          className='block px-4 py-2 text-sm text-gray-700 hover:bg-gray-200 transition duration-[var(--duration)]'
        >
          {label}
        </Link>
      ))}
      <button
        onClick={logout}
        className='w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-gray-200 duration-[var(--duration)] cursor-pointer'
      >
        Log Out
      </button>
    </div>
  );
};

export default AvatarDropdown;
