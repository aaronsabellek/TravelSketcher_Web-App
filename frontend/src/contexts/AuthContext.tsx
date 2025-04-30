import { createContext, useContext, useState, ReactNode, useEffect } from 'react';
import { useRouter } from 'next/router';
import { toast } from 'sonner';

import { BASE_URL } from '@/utils/config';
import { UserProfile } from '@/types/models';

type AuthContextType = {
  user: UserProfile | null;
  isLoggedIn: boolean;
  login: (user: UserProfile) => void;
  logout: () => void;
  isLoading: boolean;
  setIsLoggedIn: (value: boolean) => void;
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Handling login/logout-status of user
export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<UserProfile | null>(null);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();

  // Check user status
  useEffect(() => {
    const checkLogin = async () => {
      try {
        const res = await fetch(`${BASE_URL}/user/profile`, {
          credentials: 'include',
        });
        if (res.ok) {
          const data = await res.json();
          setUser(data);
          setIsLoggedIn(true);
        } else {
          setUser(null);
          setIsLoggedIn(false);
        }
      } catch (err) {
        console.error(err);
        toast.error('Connection to server failed.');
        setUser(null);
        setIsLoggedIn(false);
      } finally {
        setIsLoading(false);
      }
    };

    checkLogin();
  }, []);

  // Handle login
  const login = (user: UserProfile) => {
    setUser(user);
    setIsLoggedIn(true);
    router.replace('/destination/get_all');
  };

  // Handle logout
  const logout = async () => {
    try {
      await fetch(`${BASE_URL}/logout`, {
        method: 'POST',
        credentials: 'include',
      });
      toast.success('Logout successfully.');

    } catch (err) {
      console.log(err)
      toast.error('Logout failed.');

    } finally {
      setUser(null);
      setIsLoggedIn(false);
      router.replace('/login');
    }
  };

  return (
    <AuthContext.Provider value={{ user, isLoggedIn, login, logout, isLoading, setIsLoggedIn }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};