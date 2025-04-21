import { useRouter } from 'next/router';
import EntryOverview from '../../../components/EntryOverview';
import { useActivities } from '../../../hooks/useActivities';

export default function ActivitiesByDestination() {
  const router = useRouter();
  const { id } = router.query;

  // Wenn ID noch nicht verfügbar ist (z.B. während des Ladevorgangs)
  if (typeof id !== 'string') return <div>Lade Aktivitäten...</div>;

  // Hier nutzen wir die useActivities Hook mit der destinationId
  const {
    items,
    setItems,
    loading,
    error,
    destinationTitle,
    destinationCountry,
  } = useActivities(id);  // ID wird hier übergeben

  // Ladezustand anzeigen
  if (loading) return <div>Lade Aktivitäten...</div>;

  // Fehlerzustand
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