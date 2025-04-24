import EntryPage from '@/components/EntryForm/EntryPage';
import { useRedirectIfNotAuthenticated } from '@/hooks/authRedirects';

// Edit destination page
const EditDestinationPage = () => {

  // Redirect user if he is not logged in
  const { isReady } = useRedirectIfNotAuthenticated();
  if (!isReady) return null;

  return (
    <EntryPage
      mode='edit'
      type='destination'
    />
  );
};

export default EditDestinationPage;