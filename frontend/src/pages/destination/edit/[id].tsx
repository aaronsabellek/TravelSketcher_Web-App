import EntryPage from '../../../components/EntryForm/EntryPage';
import { useRedirectIfNotAuthenticated } from '../../../utils/authRedirects';

const EditDestinationPage = () => {
  const { isReady } = useRedirectIfNotAuthenticated();
  if (!isReady) return null;

  return <EntryPage mode="edit" type="destination" />;
};

export default EditDestinationPage;