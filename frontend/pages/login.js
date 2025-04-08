import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import { login } from '../services/api';

export default function LoginPage() {
  const [identifier, setIdentifier] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    // Check if user is already logged in
    const checkLoginStatus = async () => {
      const res = await fetch('/user/profile', { credentials: 'include' });

      if (res.ok) {
        // Push to user profile
        router.push('/user/profile');
      }

      setLoading(false); // Ladeanzeige beenden, sobald die Überprüfung abgeschlossen ist
    };

    checkLoginStatus();
  }, [router]);


  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(''); // Fehler zurücksetzen

    try {
      const response = await login(identifier, password);

      // Überprüfen, ob die Antwort korrekt ist
      if (response.message === 'Login successfull!') {
        router.push('/user/profile'); // Weiterleitung zur Profil-Seite
      } else {
        setError('Login fehlgeschlagen');
      }
    } catch (err) {
      setError(err.message); // Fehler anzeigen
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
}