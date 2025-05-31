'use client';
import React, { useState } from 'react';
import axios from 'axios';
import { useAuth } from '@/src/contexts/AuthContext';
import { useCsrf } from '@/src/hooks/useCsrf';
import { useRouter } from 'next/navigation';
import { Eye, EyeClosed } from 'lucide-react';

const LoginPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [processingLoginRequest, setProcessingLoginRequest] = useState(false); // This monitors API request
  const [redirecting, setRedirecting] = useState<boolean>(false); // Separates successful API request and router push
  const [showPassword, setShowPassword] = useState<boolean>(false);
  const { isReady, token } = useCsrf();

  const { refreshProfile, loading } = useAuth();
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setProcessingLoginRequest(true);
    if (!isReady || !token) return;
    try {
      await axios.post(
        'http://localhost:8000/api/v1/auth/login/',
        { email, password },
        {
          withCredentials: true,
          headers: {
            'X-CSRFToken': token,
            'Content-Type': 'application/json',
          },
        }
      );
      await refreshProfile();
      setRedirecting(true);
      router.push('/dashboard');
    } catch (error) {
      console.error('Login error:', error);
      alert('Login failed. Check your credentials.');
    } finally {
      setProcessingLoginRequest(false);
    }
  };

  return (
    <div className='min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900 px-4'>
      <div className='w-full max-w-md bg-white dark:bg-gray-800 shadow-md rounded-lg overflow-hidden'>
        <div className='px-6 py-4 border-b border-gray-200 dark:border-gray-700'>
          <h2 className='text-2xl font-bold text-white'>Login</h2>
          <p className='text-sm text-gray-400'>
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
            <div className='relative'>
              <input
                type={showPassword ? 'text' : 'password'}
                id='password'
                className='w-full px-3 py-2 pr-10 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500'
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
              <button
                type='button'
                className='absolute right-2 top-1/2 transform -translate-y-1/2 text-gray-500 hover:text-gray-600 cursor-pointer'
                onClick={() => setShowPassword((prev) => !prev)}
                aria-label='Toggle password visibility'
              >
                {showPassword ? <Eye /> : <EyeClosed />}
              </button>
            </div>
          </div>

          <button
            type='submit'
            disabled={processingLoginRequest}
            className='w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-md transition disabled:opacity-60 cursor-pointer'
          >
            {processingLoginRequest ? 'Logging in...' : 'Sign in'}
          </button>
        </form>

        <div className='px-6 pb-6 pt-2 border-t border-gray-200 dark:border-gray-700 text-sm text-gray-600 dark:text-gray-400'>
          <p className='text-center'>Demo Accounts:</p>
          <div className='mt-2 space-y-2 text-xs'>
            <div className='bg-gray-100 dark:bg-gray-700 p-2 rounded'>
              <strong>Admin:</strong> webdevelopmenthamilton@gmail.com / test123
            </div>
            <div className='bg-gray-100 dark:bg-gray-700 p-2 rounded'>
              <strong>Member:</strong> bob@hhsc.ca / testbob123
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
