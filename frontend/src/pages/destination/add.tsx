import EntryPage from '@/components/EntryForm/EntryPage';
import { useRedirectIfNotAuthenticated } from '@/hooks/authRedirects';

// Add destination page
const AddDestinationPage = () => {

  // Redirect user if he is not logged in
  const { isReady } = useRedirectIfNotAuthenticated();
  if (!isReady) return null;

  return (
    <EntryPage
      mode='add'
      type='destination'
    />
  );
};

export default AddDestinationPage;