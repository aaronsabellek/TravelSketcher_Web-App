import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import { useRedirectIfNotAuthenticated } from '../../utils/authRedirects';
import Container from '../../components/Container';
import BASE_URL from '../../utils/config';

interface User {
  username: string;
  city: string;
  country: string;
}

const Profile: React.FC = () => {
  const [user, setUser] = useState<User | null>(null);
  const [error, setError] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(true);
  const router = useRouter();

  // Redirect user if not authenticated
  useRedirectIfNotAuthenticated();

  // Fetch user profile
  useEffect(() => {
    const fetchUserProfile = async () => {

      try {
        const res = await fetch(`${BASE_URL}/user/profile`, {
          credentials: 'include', // Inlcude cookies
        });

        if (!res.ok) {
          const err = await res.json();
          setError(err?.error || 'Fehler beim Abrufen des Profils');
        } else {
          const data = await res.json();
          setUser(data);
        }
      } catch (err) {
        setError('Serverfehler oder keine Antwort erhalten.');
      } finally {
        setLoading(false);
      }
    };

    fetchUserProfile();
  }, [router]);

  // Loading display
  if (loading) {
    return <div>Profil wird geladen...</div>;
  }

  // Error display
  if (error) {
    return <div style={{ color: 'red' }}>Fehler: {error}</div>;
  }

  // If no user was found
  if (!user) {
    return <div>No user found.</div>;
  }

  // Show profile data
  return (
    <Container title="User profile">
      <p>Username: {user.username}</p>
      <p>City: {user.city}</p>
      <p>Country: {user.country}</p>
    </Container>
  );
};

export default Profile;