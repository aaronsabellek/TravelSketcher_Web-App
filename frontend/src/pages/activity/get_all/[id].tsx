import { useRouter } from 'next/router';

import EntryOverview from '@/components/EntryOverview';
import { useActivities } from '@/hooks/useActivities';
import { useRedirectIfNotAuthenticated } from '@/hooks/authRedirects';

// Show all activities page
export default function ActivitiesByDestination() {

  // Redirect user if he is not logged in
  const { isReady } = useRedirectIfNotAuthenticated();

  const router = useRouter();

  // Get destination id from query
  const { id } = router.query;

  // Get activity data with the destination ID
  const {
    items,
    setItems,
    loading,
    error,
    destinationTitle,
    destinationCountry,
  } = useActivities(typeof id === 'string' ? id : undefined);

  // Wait until authentication state is ready
  if (!isReady) return null;

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