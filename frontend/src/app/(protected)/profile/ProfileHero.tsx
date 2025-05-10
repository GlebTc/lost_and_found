'use client';
import { useAuth } from '@/src/contexts/AuthContext';

const ProfileHero = () => {
    const { profile } = useAuth();
    console.log(profile)
  return (
    <div>ProfileHero</div>
  )
}

export default ProfileHero