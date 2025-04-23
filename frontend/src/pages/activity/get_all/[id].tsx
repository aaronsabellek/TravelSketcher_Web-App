import { useRouter } from 'next/router';
import EntryOverview from '../../../components/EntryOverview';
import { useActivities } from '../../../hooks/useActivities';
import { useRedirectIfNotAuthenticated } from '../../../utils/authRedirects';

export default function ActivitiesByDestination() {
  const { isReady } = useRedirectIfNotAuthenticated();

  const router = useRouter();
  const { id } = router.query;

  // Hier nutzen wir die useActivities Hook mit der destinationId
  const {
    items,
    setItems,
    loading,
    error,
    destinationTitle,
    destinationCountry,
  } = useActivities(typeof id === 'string' ? id : undefined);  // ID wird hier übergeben

  if (!isReady) return null;
  if (loading) return <div>Lade Aktivitäten...</div>;
  if (error) return <div>{error}</div>;

  // Weitergabe der Daten an EntryOverview
  return (
    <EntryOverview
      title={`Activities in ${destinationTitle || '...'}, ${destinationCountry || ''} `}
      fetchHook={() => ({ items, setItems, loading, error })}
      addRoute={`/activity/add/${id}`}
      routeBase='/activity'
      showUserCity={false}
      type='activity'
    />
  );
}