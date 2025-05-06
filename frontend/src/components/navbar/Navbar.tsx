'use client';
import Link from 'next/link';
import { useState } from 'react';
import Image from 'next/image';
import hhs_logo from '@/public/images/logo/hhs_logo.webp';
import { useAuth } from '@/src/contexts/AuthContext';

const Navbar = () => {
  const componentName="NAVBAR"
  const { isAuthenticated, profile, loading } = useAuth();

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
      <div className={`${componentName}_CONTENT_CONTAINER w-fit flex items-center justify-end gap-8`}>
        {isAuthenticated && <Link href="/" className='text-gray-500 hover:text-gray-700 cursor-pointer duration-[var(--duration)]'>Lost Items</Link>}
        {isAuthenticated && <Link href="/" className='text-gray-500 hover:text-gray-700 cursor-pointer duration-[var(--duration)]'>Found Items</Link>}
        <Link
          href={`${isAuthenticated ? '/logout' : '/login'}`}
          className='text-[var(--main-color)] border-1 border-[var(--main-color)] px-4 py-2 rounded-md hover:bg-gray-300 cursor-pointer duration-[var(--duration)]'
        >
          {isAuthenticated ? 'Log Out' : 'Log In'}
        </Link>
      </div>
    </nav>
  );
};

export default Navbar;
