import { useEffect, useState } from 'react';

import { BASE_URL } from '@/utils/config';

// Get city from user
export const useUserCity = () => {

  const [city, setCity] = useState<string | null>(null);
  const [loadingCity, setLoadingCity] = useState<boolean>(true);
  const [errorCity, setErrorCity] = useState<string | null>(null);

  useEffect(() => {
    const fetchCity = async () => {
      try {
        const res = await fetch(`${BASE_URL}/user/profile`, {
          method: 'GET',
          credentials: 'include',
        });

        if (!res.ok) throw new Error('Error retrieving city');
        const data = await res.json();

        if (data.city) {
          setCity(data.city);
        } else {
          throw new Error('City not present');
        }
      } catch (err) {
        console.error(err);
        setErrorCity('City could not be loaded');
      } finally {
        setLoadingCity(false);
      }
    };

    fetchCity();
  }, []);

  return { city, loadingCity, errorCity };
};