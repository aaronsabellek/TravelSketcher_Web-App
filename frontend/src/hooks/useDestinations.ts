import { useState, useEffect, useCallback } from 'react';

import { Destination } from '@/types/models';
import { BASE_URL } from '@/utils/config';

// Administer destination
export function useDestinations() {
  const [items, setItems] = useState<Destination[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [loadingMore, setLoadingMore] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState<number>(1);
  const [hasMore, setHasMore] = useState<boolean>(true);

  // Fetch destinations from user
  const fetchDestinations = useCallback(async (pageToLoad = 1) => {
    try {
      const response = await fetch(`${BASE_URL}/destination/get_all?page=${pageToLoad}&per_page=12`, {
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error('Error loading destinations');
      }

      const data = await response.json();

      if (pageToLoad === 1) {
        setItems(data.destinations);
      } else {
        setItems(prev => [...prev, ...data.destinations]);
      }

      setHasMore(data.has_more);
    } catch (err) {
      console.error('Error loading destinations:', err);
      setError('Error loading destinations');
    } finally {
      setLoading(false);
      setLoadingMore(false);
    }
  }, []);

  // Start loading destinations
  useEffect(() => {
    fetchDestinations(1);
  }, [fetchDestinations]);

  // Load more destinations ...
  const loadMore = () => {
    if (loadingMore || !hasMore) return;
    setLoadingMore(true);
    const nextPage = page + 1;
    setPage(nextPage);
    fetchDestinations(nextPage);
  };

  // ... when user scrolls to bottom
  useEffect(() => {
    const handleWindowScroll = () => {
      const scrollTop = window.scrollY;
      const windowHeight = window.innerHeight;
      const fullHeight = document.documentElement.scrollHeight;

      if (scrollTop + windowHeight >= fullHeight - 50 && hasMore && !loadingMore) {
        loadMore();
      }
    };

    window.addEventListener('scroll', handleWindowScroll);

    return () => {
      window.removeEventListener('scroll', handleWindowScroll);
    };
  }, [hasMore, loadingMore, loadMore]);

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