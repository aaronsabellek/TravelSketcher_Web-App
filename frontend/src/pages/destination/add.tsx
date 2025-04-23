import EntryPage from '../../components/EntryForm/EntryPage';
import { useRedirectIfNotAuthenticated } from '../../utils/authRedirects';

const AddDestinationPage = () => {
  const { isReady } = useRedirectIfNotAuthenticated();
  if (!isReady) return null;

  return <EntryPage mode="add" type="destination" />;
};

export default AddDestinationPage;