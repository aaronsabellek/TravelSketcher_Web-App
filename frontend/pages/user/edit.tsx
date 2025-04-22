import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import { toast } from 'sonner';
import Container from '../../components/Container';
import { BASE_URL } from '../../utils/config';
import { useRedirectIfNotAuthenticated } from '../../utils/authRedirects';
import { UserProfile } from '../../types/models';
import Link from 'next/link';

export default function EditUserProfile() {
  const router = useRouter();
  const [userData, setUserData] = useState<Pick<UserProfile, 'username' | 'email' |'city' | 'country'>>({
    username: '',
    email: '',
    city: '',
    country: '',
  });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');

  useRedirectIfNotAuthenticated();

  // Lade aktuelle Userdaten
  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const res = await fetch(`${BASE_URL}/user/profile`, {
          credentials: 'include',
        });

        if (!res.ok) throw new Error('Error loading profile');

        const data = await res.json();
        setUserData({
          username: data.username || '',
          email: data.email,
          city: data.city || '',
          country: data.country || '',
        });
      } catch (err) {
        toast.error('Profile could not be loaded.');
      } finally {
        setLoading(false);
      }
    };

    fetchProfile();
  }, []);

  // Formularänderungen
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setUserData({ ...userData, [e.target.name]: e.target.value });
  };

  // Speichern
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);

    try {
      const res = await fetch(`${BASE_URL}/user/edit`, {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(userData),
      });

      if (!res.ok) throw new Error('Fehler beim Speichern');

      toast.success('Profile edited successfully.')
      router.push('/user/profile');
    } catch (err) {
      toast.error('Änderung fehlgeschlagen.');
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <div>Load user data...</div>;

  return (
    <Container title="Edit profile">
      <form onSubmit={handleSubmit} className="space-y-4 max-w-md mx-auto">
        {error && <p className="text-red-600">{error}</p>}

        <div>
          <label className="block text-sm font-medium text-gray-700">Username (<span className="text-red-500">*</span>required)</label>
          <input
            name="username"
            value={userData.username}
            onChange={handleChange}
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm bg-white"
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">City (<span className="text-red-500">*</span>required)</label>
          <input
            name="city"
            value={userData.city}
            onChange={handleChange}
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm bg-white"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">Country</label>
          <input
            type="text"
            name="country"
            value={userData.country ?? ''}
            onChange={handleChange}
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm bg-white"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">Email</label>
          <p className="text-gray-600 mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm">{userData.email}</p>
        </div>

        <div>
          <Link href="/user/edit_email">
            <button className="text-blue-600 hover:underline text-sm cursor-pointer">
              Edit Email
            </button>
          </Link>
        </div>

        <div>
          <Link href="/user/edit_password">
            <button className="text-blue-600 hover:underline text-sm cursor-pointer">
              Edit Password
            </button>
          </Link>
        </div>
        <div className="flex flex-col items-center space-x-4">
            <button
              type="submit"
              disabled={userData.username.trim() === '' || userData.city.trim() === '' || saving}
              className={`bg-blue-600 text-white px-5 py-2 rounded hover:bg-blue-700 transition${
                  userData.username.trim() === '' || userData.city.trim() === '' || saving
                  ? 'bg-gray-300 text-gray-500 opacity-50 cursor-not-allowed'
                  : 'bg-blue-500 text-white hover:bg-blue-600 cursor-pointer'
              }`}
            >
              {saving ? 'Saving...' : 'Save changes'}
            </button>

            <Link href="/user/profile">
              <button
                  type="button"
                  className="px-5 py-2 cursor-pointer rounded text-red-500 hover:text-red-600"
              >
                  Cancel
              </button>
            </Link>
        </div>
      </form>
    </Container>
  );
}