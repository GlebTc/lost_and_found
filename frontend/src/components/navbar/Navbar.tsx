'use client';

import Link from 'next/link';
import { useState } from 'react';
import Image from 'next/image';
import hhs_logo from '@/public/images/logo/hhs_logo.webp';

const Navbar = () => {
  // Mock auth logic – replace with actual auth hook/context
  const isAuthenticated = true; // ← make dynamic later
  const user = { name: 'Alice', avatar: '', role: 'user' }; // ← mock user
  const logout = () => alert('Logging out...'); // ← replace with real function

  const [dropdownOpen, setDropdownOpen] = useState(false);

  return (
    <nav className='bg-gray-100 fixed w-full h-[var(--navbar-h)] flex justify-between items-center px-4 md:px-20 border-b-1 border-gray-500'>
      {/* Left: Logo */}
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
      <Link href='/login' className='text-[var(--main-color)] border-1 border-[var(--main-color)] px-4 py-2 rounded-md hover:bg-gray-300 cursor-pointer duration-[var(--duration)]'>Log In</Link>
    </nav>
  );
};

export default Navbar;
