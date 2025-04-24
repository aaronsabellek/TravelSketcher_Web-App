import EntryPage from '@/components/EntryForm/EntryPage';
import { useRedirectIfNotAuthenticated } from '@/hooks/authRedirects';

// Edit activity page
const EditActivityPage = () => {

  // Redirect user if he is not logged in
  const { isReady } = useRedirectIfNotAuthenticated();
  if (!isReady) return null;

  return (
    <EntryPage
      mode='edit'
      type='activity'
    />
  );
};

export default EditActivityPage;