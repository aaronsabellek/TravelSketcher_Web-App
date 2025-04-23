import { useDestinations } from '../../hooks/useDestinations';
import EntryOverview from '../../components/EntryOverview';
import { useRedirectIfNotAuthenticated } from '../../utils/authRedirects';

export default function Destinations() {
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