import EntryPage from '@/components/EntryForm/EntryPage';
import { useRedirectIfNotAuthenticated } from '@/hooks/authRedirects';

// Add activity page
const AddActivityPage = () => {

  // Redirect user if he is not logged in
  const { isReady } = useRedirectIfNotAuthenticated();
  if (!isReady) return null;

  return (
    <EntryPage
      mode='add'
      type='activity'
    />
  );
};

export default AddActivityPage;