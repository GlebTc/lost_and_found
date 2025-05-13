'use client';
import { useFoundItems } from '@/src/hooks/useFoundItems';
import FoundHeader from './FoundHeader';
import FoundItemsList from './FoundItemsList';
import FoundSearchBar from './FoundSearchBar';

const FoundMain = () => {
  const page = 1;
  const searchTerm = '';
  const { data, isLoading, isError } = useFoundItems(page, searchTerm);

  return (
    <div className='px-12 text-gray-800 pt-[calc(var(--navbar-h)+20px)] bg-gray-200 min-h-screen'>
      <FoundHeader />
      <FoundSearchBar />
      {isLoading && <p>Loading items...</p>}
      {isError && <p>Something went wrong</p>}
      {data && <FoundItemsList items={data.results} />}
    </div>
  );
};

export default FoundMain;
