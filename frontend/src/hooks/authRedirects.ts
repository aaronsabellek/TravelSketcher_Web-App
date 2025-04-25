import { useEffect } from 'react';
import { useRouter } from 'next/router';

import { useAuth } from '@/contexts/AuthContext';

// Redirect user to start page if he is authenticated
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

// REdirect user to login page if he is not authenticated
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