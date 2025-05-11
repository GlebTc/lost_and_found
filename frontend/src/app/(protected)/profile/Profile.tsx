'use client';
import { useState } from 'react';
import { useAuth } from '@/src/contexts/AuthContext';
import { Pencil } from 'lucide-react';
import axios from 'axios';
import Loading from '@/src/components/reusable/Loading';

const Profile = () => {
  const componentName = 'Profile';
  const { profile, refreshProfile, logout } = useAuth();
  const [isEditing, setIsEditing] = useState<boolean>(false);
  const [profileData, setProfileData] = useState({
    first_name: profile?.first_name || '',
    last_name: profile?.last_name || '',
    email: profile?.email || '',
    current_password: '',
    new_password: '',
  });
  const [isLoading, setIsLoading] = useState<boolean>(false);

  if (!profile) {
    return <div>Please log in to view your profile.</div>;
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    // deconstruct name and value out of the target.
    const { name, value } = e.target;
    setProfileData((prev) => ({
      // spread previous state of profile data and add a new key(name)/value(value) pair to ProfileData
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e: any) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      await axios.patch(
        'http://localhost:8000/api/v1/accounts/profile/',
        profileData,
        { withCredentials: true }
      );
      await refreshProfile();
      setIsEditing(false);
      setIsLoading(false);
    } catch (err: any) {
      console.log(err);
      alert('Failed to update profile');
    }
  };


  return (
    <section className='max-w-2xl mx-auto grid border-2 border-gray-300 p-8 rounded-md gap-8'>
      {isLoading && <Loading message="Updating Profile" />}
      <div
        className={`${componentName}_COMPONENT_HEADER_CONTAINER flex justify-between`}
      >
        <div className={`${componentName}_HEADER_HEADING_CONTAINER`}>
          <h2>Profile</h2>
          <p className='text-gray-500'>
            View and edit your profile information
          </p>
        </div>
        <div className={`${componentName}_HEADER_BUTTONS_CONTAINER`}>
          {isEditing ? (
            <div className='flex gap-2'>
              <button
                className='button_main flex gap-4 bg-red-300'
                onClick={() => setIsEditing(false)}
              >
                Cancel
              </button>
              <button
                className='button_main flex gap-4 bg-green-300'
                onClick={handleSubmit}
              >
                Save Changes
              </button>
            </div>
          ) : (
            <button
              className='button_main flex gap-4'
              onClick={() => setIsEditing(true)}
            >
              <Pencil /> <p>Edit Profile</p>
            </button>
          )}
        </div>
      </div>
      <div
        className={`${componentName}_AVATAR AND USER INFO_CONTAINER flex gap-4`}
      >
        <div className={`${componentName}_AVATAR_CONTAINER`}>
          {profile?.avatar_url ? (
            <img
              src={profile.avatar_url}
              alt='User Avatar'
              className='w-20 h-20 rounded-full object-cover border border-gray-400'
            />
          ) : (
            <div className='w-20 h-20 rounded-full bg-cyan-700 hover:bg-cyan-600 text-white flex items-center justify-center text-6xl font-bold transition duration-[var(--duration)]'>
              {profile?.first_name
                ? profile.first_name[0].toUpperCase()
                : profile?.email[0].toUpperCase()}
            </div>
          )}
        </div>
        <div className={`${componentName}_USER_INFO_CONTAINER`}>
          <h3>
            {profile.first_name} {profile.last_name}
          </h3>
          <p className='text-gray-500'>{profile.role}</p>
          <p className='text-gray-500'>{profile.email}</p>
        </div>
      </div>
      <form className={`${componentName}_EDITABLE_FORM_CONTAINER space-y-4`}>
        <div className='grid'>
          <label htmlFor='first_name'>
            <h4>First Name</h4>
          </label>
          <input
            type='text'
            id='first_name'
            name='first_name'
            value={profileData.first_name ?? ''}
            onChange={handleChange}
            disabled={!isEditing}
            className={`border-2 border-gray-300 rounded-md p-2 text-gray-500 ${
              isEditing ? 'bg-gray-100' : 'bg-gray-200'
            } focus:text-black focus:bg-white focus:border-blue-500 focus:outline-none`}
          />
        </div>
        <div className='grid'>
          <label htmlFor='last_name'>
            <h4>Last Name</h4>
          </label>
          <input
            type='text'
            id='last_name'
            name='last_name'
            value={profileData.last_name ?? ''}
            onChange={handleChange}
            disabled={!isEditing}
            className={`border-2 border-gray-300 rounded-md p-2 text-gray-500 ${
              isEditing ? 'bg-gray-100' : 'bg-gray-200'
            } focus:text-black focus:bg-white focus:border-blue-500 focus:outline-none`}
          />
        </div>
        <div className='grid'>
          <label htmlFor='email'>
            <h4>Email</h4>
          </label>
          <input
            type='text'
            id='email'
            name='email'
            value={profileData.email ?? ''}
            onChange={handleChange}
            disabled={!isEditing}
            className={`border-2 border-gray-300 rounded-md p-2 text-gray-500 ${
              isEditing ? 'bg-gray-100' : 'bg-gray-200'
            } focus:text-black focus:bg-white focus:border-blue-500 focus:outline-none`}
          />
        </div>
        {isEditing && (
          <div className='space-y-4'>
            <div className='grid'>
              <label htmlFor='current_password'>
                <h4>Current Password</h4>
              </label>
              <input
                type='password'
                id='current_password'
                name='current_password'
                value={profileData.current_password}
                onChange={handleChange}
                className='border-2 border-gray-300 rounded-md p-2 bg-gray-100 focus:text-black focus:bg-white focus:border-blue-500 focus:outline-none'
              />
            </div>
            <div className='grid'>
              <label htmlFor='new_password'>
                <h4>New Password</h4>
              </label>
              <input
                type='password'
                id='new_password'
                name='new_password'
                value={profileData.new_password}
                onChange={handleChange}
                className='border-2 border-gray-300 rounded-md p-2 bg-gray-100 focus:text-black focus:bg-white focus:border-blue-500 focus:outline-none'
              />
            </div>
          </div>
        )}
      </form>

      <div
        className={`${componentName}_DELETE_AND_LOGOUT_CONTAINER border-t-2 pt-6 border-gray-300`}
      >
        <button
          onClick={logout}
          className='button_main'
        >
          <p className='text-red-500'>Log Out</p>
        </button>
      </div>
    </section>
  );
};

export default Profile;
