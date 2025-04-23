import { useEffect, useState, useCallback } from 'react';
import { useRouter } from 'next/router';
import { toast } from 'sonner';
import { BASE_URL } from '../utils/config';

export type EntryFormData = {
  title?: string;
  country?: string;
  tags?: string[];
  img_link?: string;
  destination_id?: string;
};

export function useEntryFormHandler(mode: 'add' | 'edit', type: 'destination' | 'activity') {
  const router = useRouter();
  const rawId = router.query.id as string | undefined;

  const [initialData, setInitialData] = useState<EntryFormData | null>(null);
  const [destinationId, setDestinationId] = useState<string | null>(null);

  const fetchItemData = useCallback(async () => {
    const endpoint = `${BASE_URL}/${type}/get/${rawId}`;
    try {
      const res = await fetch(endpoint, { credentials: 'include' });
      const data = await res.json();
      const itemData = data[type];

      if (typeof itemData.tags === 'string') {
        itemData.tags = itemData.tags
          .split(',')
          .map((tag: string) => tag.trim())
          .filter((tag: string) => tag.length > 0);
      }

      setInitialData(itemData);

      if (type === 'activity' && itemData.destination_id) {
        setDestinationId(itemData.destination_id);
      }
    } catch (err) {
      console.error(err);
      toast.error('Fehler beim Laden.');
    }
  }, [rawId, type]);

  const handleAddActivityDestination = () => {
    if (type === 'activity' && rawId) {
      setDestinationId(rawId);
    }
  };

  useEffect(() => {
    if (!router.isReady || !rawId) return;

    if (mode === 'edit') {
      fetchItemData();
    } else if (mode === 'add') {
      handleAddActivityDestination();
    }
  }, [router.isReady, mode, rawId, type, fetchItemData]);

  const getEndpoint = (): string | null => {
    if (mode === 'add' && type === 'destination') {
      return `${BASE_URL}/destination/add`;
    }

    if (mode === 'add' && type === 'activity') {
      if (!destinationId) {
        toast.error('Destination ID fehlt.');
        return null;
      }
      return `${BASE_URL}/activity/add/${destinationId}`;
    }

    if (mode === 'edit') {
      if (!rawId) {
        toast.error('ID fehlt.');
        return null;
      }
      return `${BASE_URL}/${type}/edit/${rawId}`;
    }

    toast.error('Unbekannter Modus oder Typ.');
    return null;
  };

  const handleSubmit = async (formData: EntryFormData) => {
    if (!router.isReady) {
      toast.error('Router ist noch nicht bereit.');
      return;
    }

    const endpoint = getEndpoint();
    if (!endpoint) return;

    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      if (!response.ok) throw new Error('Fehler beim Speichern');

      toast.success(mode === 'add' ? 'Erfolgreich hinzugefügt!' : 'Erfolgreich aktualisiert!');

      const pushRoute =
        type === 'destination'
          ? `/destination/get_all`
          : `/activity/get_all/${destinationId}`;

      router.push(pushRoute);
    } catch (err) {
      console.error(err);
      toast.error('Fehler beim Speichern.');
    }
  };

  return {
    initialData,
    handleSubmit,
  };
}