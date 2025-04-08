import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';

interface User {
  username: string;
  city: string;
  country: string;
}

const ProfilePage: React.FC = () => {
  const [user, setUser] = useState<User | null>(null);
  const [error, setError] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(true);
  const router = useRouter();

  // Fetch user profile
  useEffect(() => {
    const fetchUserProfile = async () => {
      try {
        const res = await fetch('http://localhost:5000/user/profile', {
          credentials: 'include', // Inlcude cookies
        });

        if (!res.ok) {
          // If user is not logged in, push to login page
          router.push('/login');
          return;
        }

        const data = await res.json();
        setUser(data);
      } catch (err) {
        console.error('Error:', err);
        setError('Server error or no response received');
      } finally {
        setLoading(false);
      }
    };

    fetchUserProfile();
  }, [router]);

  // Funktion zum Ausloggen
  const handleLogout = async () => {
    try {
      const res = await fetch('http://localhost:5000/logout', {
        method: 'POST',
        credentials: 'include', // Include cookies
      });

      if (res.ok) {
        // After logout push to login page
        router.push('/login');
      } else {
        setError('Logout failed.');
      }
    } catch (err) {
      console.error('Logout Error:', err);
      setError('Server error or no response received.');
    }
  };

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
    <div>
      <h1>User profile</h1>
      <p>Username: {user.username}</p>
      <p>City: {user.city}</p>
      <p>Country: {user.country}</p>

      {/* Logout Button */}
      <button onClick={handleLogout}>Logout</button>
    </div>
  );
};

export default ProfilePage;