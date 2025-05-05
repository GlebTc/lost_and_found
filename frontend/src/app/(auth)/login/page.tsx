'use client';
import React, { useState } from 'react';
import axios from 'axios';
import Loading from '@/src/components/reusable/Loading';

const LoginPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    const loginResponse = await axios.post(
      'http://localhost:8000/api/v1/auth/login/',
      {
        email: email,
        password: password,
      },
      { withCredentials: true } 
    );
    console.log("response:", loginResponse.data)
    setTimeout(() => {
      setIsLoading(false);
      alert(`Logged in as ${email}`);
    }, 1500);
  };

  if (isLoading) return <Loading message="Checking Credentials..."/>;

  return (
    <div className='min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900 px-4'>
      <div className='w-full max-w-md bg-white dark:bg-gray-800 shadow-md rounded-lg overflow-hidden'>
        <div className='px-6 py-4 border-b border-gray-200 dark:border-gray-700'>
          <h2 className='text-2xl font-bold text-gray-900 dark:text-white'>
            Login
          </h2>
          <p className='text-sm text-gray-600 dark:text-gray-400'>
            Enter your credentials to access the lost and found system
          </p>
        </div>
        <form
          onSubmit={handleSubmit}
          className='px-6 py-6 space-y-4'
        >
          <div className='space-y-2'>
            <label
              htmlFor='email'
              className='block text-sm font-medium text-gray-700 dark:text-gray-300'
            >
              Email
            </label>
            <input
              type='email'
              id='email'
              className='w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500'
              placeholder='email@example.com'
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div className='space-y-2'>
            <label
              htmlFor='password'
              className='block text-sm font-medium text-gray-700 dark:text-gray-300'
            >
              Password
            </label>
            <input
              type='password'
              id='password'
              className='w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500'
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <button
            type='submit'
            disabled={isLoading}
            className='w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-md transition disabled:opacity-60 cursor-pointer'
          >
            {isLoading ? 'Logging in...' : 'Sign in'}
          </button>
        </form>

        <div className='px-6 pb-6 pt-2 border-t border-gray-200 dark:border-gray-700 text-sm text-gray-600 dark:text-gray-400'>
          <p className='text-center'>Demo Accounts:</p>
          <div className='mt-2 space-y-2 text-xs'>
            <div className='bg-gray-100 dark:bg-gray-700 p-2 rounded'>
              <strong>Admin:</strong> webdevelopmenthamilton@gmail.com / test123
            </div>
            <div className='bg-gray-100 dark:bg-gray-700 p-2 rounded'>
              <strong>Moderator:</strong> mod@example.com / mod123
            </div>
            <div className='bg-gray-100 dark:bg-gray-700 p-2 rounded'>
              <strong>Member:</strong> member@example.com / member123
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
