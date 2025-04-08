import { useEffect, useState } from 'react';

const ProfilePage = () => {
  const [user, setUser] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchUserProfile = async () => {
      try {
        const res = await fetch('http://localhost:5000/user/profile', {
          credentials: 'include',
        });

        if (!res.ok) {
          const err = await res.json();
          setError(err?.error || 'Fehler beim Abrufen des Profils');
        } else {
          const data = await res.json();
          setUser(data);
        }
      } catch (err) {
        console.error('Fehler:', err);
        setError('Serverfehler oder keine Antwort erhalten.');
      } finally {
        setLoading(false);
      }
    };

    fetchUserProfile();
  }, []);

  if (loading) {
    return <div>Profil wird geladen...</div>;
  }

  if (error) {
    return <div style={{ color: 'red' }}>Fehler: {error}</div>;
  }

  if (!user) {
    return <div>Kein Benutzer gefunden.</div>;
  }

  return (
    <div>
      <h1>Benutzerprofil</h1>
      <p>Username: {user.username}</p>
      <p>City: {user.city}</p>
      <p>Country: {user.country}</p>
    </div>
  );
};

export default ProfilePage;