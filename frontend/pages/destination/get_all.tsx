import { useDestinations } from '../../hooks/useDestinations';
import EntryOverviewPage from '../../components/EntryOverviewPage';

export default function Destinations() {
  return (
    <EntryOverviewPage
      title="My Destinations"
      fetchHook={useDestinations}
      addRoute="/destination/add"
      showUserCity
    />
  );
};