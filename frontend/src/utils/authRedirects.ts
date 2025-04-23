import { useEffect } from 'react';
import { useRouter } from 'next/router';
import { useAuth } from '../contexts/AuthContext';

export const useRedirectIfAuthenticated = (redirectTo: string = '/destination/get_all') => {
  const { isLoggedIn, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading && isLoggedIn) {
      router.replace(redirectTo);
    }
  }, [isLoggedIn, isLoading, router, redirectTo]);

  return {
    isReady: !isLoading && !isLoggedIn,
  };
};

export const useRedirectIfNotAuthenticated = (redirectTo: string = '/login') => {
  const { isLoggedIn, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    console.log('Redirect Check:', { isLoading, isLoggedIn });
    if (!isLoading && !isLoggedIn) {
      router.replace(redirectTo);
    }
  }, [isLoggedIn, isLoading, router, redirectTo]);

  return {
    isReady: !isLoading && isLoggedIn,
  };
};