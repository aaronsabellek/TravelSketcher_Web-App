import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';

const LoginPage = () => {
  const [identifier, setIdentifier] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const router = useRouter();

  // Check if user is already logged in
  useEffect(() => {
    const checkLoginStatus = async () => {
      const res = await fetch('http://localhost:5000/user/profile', {
        credentials: 'include', // Cookies werden mitgesendet
      });

      if (res.ok) {
        // Wenn der Benutzer bereits eingeloggt ist, leite ihn auf die Profilseite weiter
        router.push('/user/profile');
      }
    };

    checkLoginStatus();
  }, [router]);

  // Login user
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    try {
      const response = await fetch('http://localhost:5000/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          identifier, // Username or Email
          password,
        }),
        credentials: 'include', // Include cookie for session
      });

      if (!response.ok) {
        const data = await response.json();
        setError(data.error || 'Login fehlgeschlagen');
        return;
      }

      // Push to user profile
      router.push('/user/profile');
    } catch (err) {
      console.error(err);
      setError('Ein Fehler ist beim Login aufgetreten.');
    }
  };

  return (
    <div className="login-container">
      <h1>Login</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="identifier">Email or Username</label>
          <input
            type="text"
            id="identifier"
            value={identifier}
            onChange={(e) => setIdentifier(e.target.value)}
            required
          />
        </div>
        <div>
          <label htmlFor="password">Password</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit">Login</button>
      </form>

      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
};

export default LoginPage;