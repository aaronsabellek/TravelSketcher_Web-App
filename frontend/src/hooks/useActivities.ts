import { useState, useEffect, useCallback } from 'react';
import { Activity } from '@/types/models';
import { BASE_URL } from '@/utils/config';

// Administer activities
export const useActivities = (destination_id?: string) => {
  const [items, setItems] = useState<Activity[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [loadingMore, setLoadingMore] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState<number>(1);
  const [hasMore, setHasMore] = useState<boolean>(true);
  const [destinationTitle, setDestinationTitle] = useState<string>('');
  const [destinationCountry, setDestinationCountry] = useState<string>('');

  // Fetch activities from specific destination
  const fetchActivities = useCallback(async (pageToLoad = 1) => {
    if (!destination_id) return;

    try {
      const res = await fetch(`${BASE_URL}/activity/get_all/${destination_id}?page=${pageToLoad}&per_page=12`, {
        credentials: 'include',
        method: 'GET',
      });

      if (!res.ok) throw new Error('Error laoding activities');

      const data = await res.json();

      if (pageToLoad === 1) {
        setItems(data.activities || []);
      } else {
        setItems(prev => [...prev, ...(data.activities || [])]);
      }

      setHasMore(data.has_more);
    } catch (err) {
      setError('Error loading activities');
      console.error(err);
    } finally {
      setLoading(false);
      setLoadingMore(false);
    }
  }, [destination_id]);

  // Start loading activities
  useEffect(() => {
    setLoading(true);
    setPage(1);
    fetchActivities(1);
  }, [fetchActivities]);

  // Load more activities ...
  const loadMore = () => {
    if (loadingMore || !hasMore || !destination_id) return;
    setLoadingMore(true);
    const nextPage = page + 1;
    setPage(nextPage);
    fetchActivities(nextPage);
  };

  // ... when user scrollt to bottom
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
    return () => window.removeEventListener('scroll', handleWindowScroll);
  }, [hasMore, loadingMore, loadMore]);

  // Get destination for activities from database
  useEffect(() => {
    if (!destination_id) return;

    const fetchDestinationName = async () => {

      try {
        const res = await fetch(`${BASE_URL}/destination/get/${destination_id}`, {
          credentials: 'include',
        });

        if (!res.ok) throw new Error('Error loading destination');

        const data = await res.json();
        setDestinationTitle(data.destination.title);
        setDestinationCountry(data.destination.country);
      } catch (err) {
        console.error(err);
        setError('Error loading destination');
      }
    };

    fetchDestinationName();
  }, [destination_id]);

  return {
    items,
    setItems,
    loading,
    error,
    loadMore,
    hasMore,
    loadingMore,
    destinationTitle,
    destinationCountry,
  };
};