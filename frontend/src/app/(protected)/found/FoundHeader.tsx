import Link from 'next/link';

const FoundHeader = () => {
  return (
    <div className='w-full flex justify-between items-center py-4 border-b-1 border-gray-300'>
      <h2>Found Items</h2>
      <Link
        href='/report-found'
        className='w-fit px-6 py-3 rounded-lg bg-cyan-900 hover:bg-cyan-800 text-white font-semibold cursor-pointer transition duration-[var(--duration)] text-center'
      >
        Report Found Item
      </Link>
    </div>
  );
};

export default FoundHeader;
