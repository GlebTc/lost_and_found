import { useEffect, useState } from 'react';
import axios from 'axios';
import { BASE_URL } from '@/src/data/constants'

function getCookie(name: string): string | null {
  const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
  return match ? match[2] : null;
}

export const useCsrf = () => {
  const [isReady, setIsReady] = useState(false);
  const [token, setToken] = useState<string | null>(null);

  useEffect(() => {
    const fetchCsrf = async () => {
      try {
        await axios.get(`${BASE_URL}/csrf/`, {
          withCredentials: true,
        });

        const cookie = getCookie('csrftoken');
        setToken(cookie);
        setIsReady(true);
      } catch (err) {
        console.error('CSRF fetch failed:', err);
      }
    };

    fetchCsrf();
  }, []);

  return { isReady, token };
};
