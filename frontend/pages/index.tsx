import { useEffect } from 'react';
import { useRouter } from 'next/router';
import { useAuth } from '../contexts/AuthContext';

const Home = () => {
  const { isLoggedIn, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading) {
      if (isLoggedIn) {
        router.push('/user/profile');
      } else {
        router.push('/about');
      }
    }
  }, [isLoggedIn, isLoading, router]);

  return <div>Loading...</div>;
};

export default Home;