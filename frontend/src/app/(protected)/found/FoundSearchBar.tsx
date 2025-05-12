'use client';
import { useState, useEffect } from 'react';
import { Search } from 'lucide-react';
import axios from 'axios';

const FoundSearchBar = () => {
  const componentName = 'FoundSearchBar';
  const [searchTerm, setSearchTerm] = useState<string>('');
  const [searchResults, setSearchResults] = useState<[]>([]);

  // http://localhost:8000/api/v1/items/search/?q=${encodeURIComponent(searchTerm)}

  useEffect(() => {
    // Delay execution by 300ms (debounce logic)
    const delayDebounce = setTimeout(() => {
      const fetchResults = async () => {
        // trim() removes spaces around input, if there is no input, trim() will returnf "".  Our if statement says if return from trim is not empty, then continue.
        if (!searchTerm.trim()) {
          setSearchResults([]);
          return;
        }

        try {
          const res = await axios.get(
            `http://localhost:8000/api/v1/items/search/?q=${encodeURIComponent(
              searchTerm
            )}`,
            { withCredentials: true }
          );
          setSearchResults(res.data);
          console.log(res.data); // For debugging
        } catch (err) {
          console.error('Search error:', err);
        }
      };

      fetchResults(); // Call the async function
    }, 300);

    // Clear the timer if searchTerm changes before 300ms
    return () => clearTimeout(delayDebounce);
  }, [searchTerm]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(e.target.value);
  };

  return (
    <div
      className={`${componentName}_MAIN_CONTAINER flex justify-between gap-8 py-4`}
    >
      <input
        type='text'
        placeholder='Search found items...'
        name='search_params'
        value={searchTerm}
        className='border-1 w-full border-gray-300 rounded-md pl-4'
        onChange={handleChange}
      />
      <button className='button_main flex gap-4 w-[200px]'>
        <Search /> <p>Search</p>
      </button>
    </div>
  );
};

export default FoundSearchBar;
