import EntryPage from '../../../components/EntryForm/EntryPage';
import { useRedirectIfNotAuthenticated } from '../../../utils/authRedirects';

const EditActivityPage = () => {
  const { isReady } = useRedirectIfNotAuthenticated();
  if (!isReady) return null;

  return <EntryPage mode="edit" type="activity" />;
};

export default EditActivityPage;