import { useDestinations } from '../../hooks/useDestinations';
import EntryOverview from '../../components/EntryOverview';

export default function Destinations() {
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