import { useEffect } from 'react';
import { useRouter } from 'next/router';
import { useAuth } from '../src/contexts/AuthContext';

const Home = () => {
  const { isLoggedIn, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading) {
      if (isLoggedIn) {
        router.push('/destination/get_all');
      } else {
        router.push('/about');
      }
    }
  }, [isLoggedIn, isLoading, router]);

  return <div>Loading...</div>;
};

export default Home;