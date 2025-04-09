import { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useRedirectIfAuthenticated } from '../utils/authRedirects';
import Link from 'next/link';
import BASE_URL from '../utils/config';

const Login = () => {
  const [identifier, setIdentifier] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const { isLoading, login } = useAuth();

  // Redirect if user is authenticated
  useRedirectIfAuthenticated();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

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
        setError(data.error || 'Login fehlgeschlagen');
        return;
      }

      const userData = await response.json();
      login(userData);

      //router.replace('/user/profile');
    } catch (err) {
      console.error(err);
      setError('Ein Fehler ist beim Login aufgetreten.');
    }
  };

  if (isLoading) {
    return <div className="text-center mt-10">Lade Authentifizierungsstatus...</div>;
  }

  return (
    <div className="max-w-md mx-auto mt-10 p-6 border rounded-lg shadow-md bg-white">
      <h1 className="text-2xl font-bold text-center mb-4">Login</h1>
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label htmlFor="identifier" className="block text-sm font-medium text-gray-700">Email or Username</label>
          <input
            type="text"
            id="identifier"
            value={identifier}
            onChange={(e) => setIdentifier(e.target.value)}
            required
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm"
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
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm"
          />
        </div>
        <button
          type="submit"
          className="w-full py-2 px-4 bg-blue-500 text-white font-semibold rounded-lg hover:bg-blue-600"
        >
          Login
        </button>
      </form>
      <p className="mt-4 text-sm text-center">
        Keine Verifizierungs-E-Mail erhalten?{' '}
        <Link href="/resend_verification">
          <span className="text-blue-600 underline cursor-pointer">
            Hier erneut senden
          </span>
        </Link>
      </p>
      {error && <p className="text-red-500 mt-4 text-center">{error}</p>}
    </div>
  );
};

export default Login;