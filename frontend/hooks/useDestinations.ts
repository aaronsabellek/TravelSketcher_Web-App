import { useState, useEffect } from 'react';
import { Destination } from '../types/models';
import { BASE_URL } from '../utils/config';

export function useDestinations() {
  const [destinations, setDestinations] = useState<Destination[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchDestinations = async () => {
      try {
        const response = await fetch(`${BASE_URL}/destination/get_all`, {
          credentials: 'include',
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        });

        if (!response.ok) {
          throw new Error('Fehler beim Laden der Destinations');
        }

        const data = await response.json();
        setDestinations(data.destinations);
      } catch (err) {
        console.error('Fehler beim Laden der Destinations:', err);
        setError('Fehler beim Laden der Destinations');
      } finally {
        setLoading(false);
      }
    };

    fetchDestinations();
  }, []);

  return {
    items: destinations,
    setItems: setDestinations,
    loading,
    error
  };
}