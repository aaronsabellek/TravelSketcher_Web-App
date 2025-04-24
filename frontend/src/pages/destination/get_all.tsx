import { useDestinations } from '@/hooks/useDestinations';
import EntryOverview from '@/components/EntryOverview';
import { useRedirectIfNotAuthenticated } from '@/hooks/authRedirects';

// Show all destinations page
export default function Destinations() {

  // Redirect user if he is not logged in
  const { isReady } = useRedirectIfNotAuthenticated();
  if (!isReady) return null;

  return (
    <EntryOverview
      title='My Destinations'
      fetchHook={useDestinations}
      addRoute='/destination/add'
      routeBase='/destination'
      showUserCity
      type="destination"
    />
  );
};