import { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useRedirectIfAuthenticated } from '../utils/authRedirects';
import Container from '../components/Container';
import Link from 'next/link';
import { BASE_URL } from '../utils/config';
import { toast } from 'sonner';

const Login = () => {
  // Redirect if user is authenticated
  const { isReady } = useRedirectIfAuthenticated();

  const [identifier, setIdentifier] = useState('');
  const [password, setPassword] = useState('');
  const { isLoading, login } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      const response = await fetch(`${BASE_URL}/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ identifier, password }),
        credentials: 'include',
      });

      if (!response.ok) {
        const data = await response.json();
        toast.error(data.error || 'Login fehlgeschlagen');
        return;
      }

      const userData = await response.json();
      login(userData);

    } catch (err) {
      toast.error('Ein Fehler ist beim Login aufgetreten.');
    }
  };

  if (isLoading) {
    return <div className="text-center mt-10">Lade Authentifizierungsstatus...</div>;
  }

  if (!isReady) return null;

  return (
    <Container title="Login">
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label htmlFor="identifier" className="block text-sm font-medium text-gray-700">Email or Username</label>
          <input
            type="text"
            id="identifier"
            value={identifier}
            onChange={(e) => setIdentifier(e.target.value)}
            required
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm bg-white"
          />
        </div>
        <div className="mb-6">
          <label htmlFor="password" className="block text-sm font-medium text-gray-700">Password</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm bg-white"
          />
        </div>
        <button
          type="submit"
          className="w-full py-2 px-4 bg-blue-500 text-white font-semibold rounded-lg cursor-pointer hover:bg-blue-600"
        >
          Login
        </button>
      </form>

      <p className="mt-4 text-sm text-center">
        Forgot password?{' '}
        <Link href="/user/forgot_password">
          <span className="text-blue-600 underline cursor-pointer">Reset here</span>
        </Link>
      </p>

      <p className="mt-4 text-sm text-center">
        No verification email received?{' '}
        <Link href="/resend_verification">
          <span className="text-blue-600 underline cursor-pointer">
            Send here again
          </span>
        </Link>
      </p>
    </Container>
  );
};

export default Login;