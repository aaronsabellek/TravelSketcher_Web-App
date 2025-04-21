import { useState, useEffect, useCallback } from 'react';
import { Destination } from '../types/models';
import { BASE_URL } from '../utils/config';

export function useDestinations() {
  const [items, setItems] = useState<Destination[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [loadingMore, setLoadingMore] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState<number>(1);
  const [hasMore, setHasMore] = useState<boolean>(true);

  const fetchDestinations = useCallback(async (pageToLoad = 1) => {
    try {
      const response = await fetch(`${BASE_URL}/destination/get_all?page=${pageToLoad}&per_page=12`, {
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error('Fehler beim Laden der Destinations');
      }

      const data = await response.json();

      if (pageToLoad === 1) {
        setItems(data.destinations);
      } else {
        setItems(prev => [...prev, ...data.destinations]);
      }

      setHasMore(data.has_more);
    } catch (err) {
      console.error('Fehler beim Laden der Destinations:', err);
      setError('Fehler beim Laden der Destinations');
    } finally {
      setLoading(false);
      setLoadingMore(false);
    }
  }, []);

  useEffect(() => {
    fetchDestinations(1);
  }, [fetchDestinations]);

  const loadMore = () => {
    if (loadingMore || !hasMore) return;
    setLoadingMore(true);
    const nextPage = page + 1;
    setPage(nextPage);
    fetchDestinations(nextPage);
  };

  // useEffect für das Scroll-Event
  useEffect(() => {
    const handleWindowScroll = () => {
      const scrollTop = window.scrollY;
      const windowHeight = window.innerHeight;
      const fullHeight = document.documentElement.scrollHeight;

      if (scrollTop + windowHeight >= fullHeight - 50 && hasMore && !loadingMore) {
        loadMore(); // Weiterladen
      }
    };

    // Scroll-Event hinzufügen
    window.addEventListener('scroll', handleWindowScroll);

    // Event-Listener aufräumen, wenn der Hook unmontiert wird
    return () => {
      window.removeEventListener('scroll', handleWindowScroll);
    };
  }, [hasMore, loadingMore, loadMore]); // Abhängigkeiten: nur neu starten, wenn hasMore oder loadingMore sich ändern

  return {
    items,
    setItems,
    loading,
    error,
    loadMore,
    hasMore,
    loadingMore,
  };
}