'use client';
import DashboardHero from './DashboardHero';

const DashboardMain = () => {
  return (
    <div className='p-8 text-gray-800 pt-[calc(var(--navbar-h)+20px)] bg-gray-200 min-h-screen'>
      <DashboardHero />
    </div>
  );
};

export default DashboardMain;
