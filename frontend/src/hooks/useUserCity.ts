import { useEffect, useState } from 'react';
import { BASE_URL } from '../utils/config';

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

        if (!res.ok) throw new Error('Fehler beim Abrufen der Stadt');
        const data = await res.json();

        if (data.city) {
          setCity(data.city);
        } else {
          throw new Error('Stadt nicht vorhanden');
        }
      } catch (err) {
        console.error('Fehler beim Laden der Stadt:', err);
        setErrorCity('Stadt konnte nicht geladen werden');
      } finally {
        setLoadingCity(false);
      }
    };

    fetchCity();
  }, []);

  return { city, loadingCity, errorCity };
};