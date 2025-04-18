import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import EntryOverviewPage from '../../../components/EntryOverviewPage';
import { useActivities } from '../../../hooks/useActivities';
import { BASE_URL } from '../../../utils/config';
import { Activity } from '../../../types/models';

export default function ActivitiesByDestination() {
  const router = useRouter();
  const { id } = router.query;

  const { items, setItems } = useActivities();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [destinationName, setDestinationName] = useState('');

  useEffect(() => {
    const fetchActivities = async () => {
      if (typeof id !== 'string') return;

      try {
        const res = await fetch(`${BASE_URL}/activity/get_all/${id}`, {
          credentials: 'include',
          method: 'GET',
        });
        const data = await res.json();

        if (data && Array.isArray(data.activities)) {
          setItems(data.activities);  // Hier setzen wir die Aktivitäten
        } else {
          setItems([]);  // Wenn kein Array vorhanden ist, setzen wir `items` auf ein leeres Array
        }

      } catch (err) {
        console.error('Fehler beim Laden der Aktivitäten:', err);
      } finally {
        setLoading(false);
      }
    };

    const fetchDestinationName = async () => {
      if (typeof id !== 'string') return;
      try {
        const res = await fetch(`${BASE_URL}/destination/${id}`, {
          credentials: 'include',
        });
        const data = await res.json();
        setDestinationName(data.name);
      } catch (err) {
        console.error('Fehler beim Laden des Namens:', err);
      }
    };

    if (id) {
      fetchActivities();
      fetchDestinationName();
    }
  }, [id]);

  if (loading || typeof id !== 'string') return <div>Lade Aktivitäten...</div>;

  return (
    <EntryOverviewPage
      title={`Aktivitäten in ${destinationName || '...'} `}
      fetchHook={() => ({ items, setItems, loading, error })}
      addRoute={`/activity/add/${id}`}
      showUserCity={false}
    />
  );
}