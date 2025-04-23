import EntryPage from '../../../components/EntryForm/EntryPage';
import { useRedirectIfNotAuthenticated } from '../../../utils/authRedirects';


const AddActivityPage = () => {
  const { isReady } = useRedirectIfNotAuthenticated();
  if (!isReady) return null;

  return <EntryPage mode="add" type="activity" />;
};

export default AddActivityPage;