// components/found/FoundItemCard.tsx
import React from 'react';

interface FoundItemCardProps {
  title: string;
  description?: string | null;
  date_found: string;
  location: string;
}

const FoundItemCard = ({
  title,
  description,
  date_found,
  location,
}: FoundItemCardProps) => {
  return (
    <div className='bg-white shadow-md rounded-lg border border-gray-200 p-6 w-full max-w-md'>
      <h3 className='text-xl font-bold text-[var(--main-color)] mb-2'>{title}</h3>
      <p className='text-gray-600 mb-2'>{description}</p>
      <p className='text-sm text-gray-500'>
        <strong>Date Found:</strong> {new Date(date_found).toLocaleDateString()}
      </p>
      <p className='text-sm text-gray-500'>
        <strong>Location:</strong> {location}</p>
    </div>
  );
};

export default FoundItemCard;
