import { useEffect } from 'react';
import { useRouter } from 'next/router';
import { useAuth } from '../contexts/AuthContext';

export const useRedirectIfAuthenticated = (redirectTo: string = '/user/profile') => {
  const { isLoggedIn, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading && isLoggedIn) {
      router.replace(redirectTo);
    }
  }, [isLoggedIn, isLoading, router, redirectTo]);
};

export const useRedirectIfNotAuthenticated = (redirectTo: string = '/login') => {
  const { isLoggedIn, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading && !isLoggedIn) {
      router.replace(redirectTo);
    }
  }, [isLoggedIn, isLoading, router, redirectTo]);
};