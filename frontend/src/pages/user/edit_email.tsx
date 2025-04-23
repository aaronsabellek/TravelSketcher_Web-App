import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import Container from '../../components/Container';
import { BASE_URL } from '../../utils/config';
import { toast } from 'sonner';
import { useRedirectIfNotAuthenticated } from '../../utils/authRedirects';

const EditEmailPage: React.FC = () => {
  const { isReady } = useRedirectIfNotAuthenticated();

  const [email, setEmail] = useState('');
  const [currentEmail, setCurrentEmail] = useState('');
  const [error, setError] = useState('');
  const [saving, setSaving] = useState(false);
  const router = useRouter();

  // Check for valid email format
  const isValidEmail = (email: string) =>
    /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);

  // Hole aktuelle E-Mail beim Laden
  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const res = await fetch(`${BASE_URL}/user/profile`, {
          credentials: 'include',
        });
        const data = await res.json();
        setCurrentEmail(data.email);
      } catch (err) {
        setError('Fehler beim Laden des Profils.');
      }
    };

    fetchProfile();
  }, []);

  // Submit Handler
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setError('');

    try {
      const res = await fetch(`${BASE_URL}/user/edit_email`, {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email }),
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.error || 'Unbekannter Fehler');
      }

      toast.success('Bestätigungs-E-Mail wurde versendet.');
      router.push('/user/profile');
    } catch (err: any) {
      setError(err.message);
      toast.error(err.message);
    } finally {
      setSaving(false);
    }
  };

  if (!isReady) return null;

  return (
    <Container title="Edit Email">
      <form onSubmit={handleSubmit} className="space-y-4 max-w-md mx-auto">
        {error && <p className="text-red-600">{error}</p>}

        <div>
          <label className="block text-sm font-medium text-gray-700">Current E-Mail</label>
          <p className="text-gray-600 mt-1 px-3 py-2 border border-gray-300 rounded-md bg-gray-100">
            {currentEmail || 'Lädt...'}
          </p>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">
            New E-Mail
          </label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm bg-white"
          />
        </div>

        <div className="flex flex-col items-center space-x-4">
          <button
            type="submit"
            disabled={!isValidEmail(email) || saving}
            className={`px-5 py-2 rounded text-white transition ${
                !isValidEmail(email) || saving
                ? 'bg-gray-400 text-gray-500 cursor-not-allowed'
                : 'bg-blue-500 text-white hover:bg-blue-600 cursor-pointer'
            }`}
          >
            {saving ? 'Sending...' : 'Send verification email'}
          </button>

          <button
            type="button"
            onClick={() => router.push('/user/profile')}
            className="px-5 py-2 cursor-pointer rounded text-red-500 hover:text-red-600"
          >
            Cancel
          </button>
        </div>
      </form>
    </Container>
  );
};

export default EditEmailPage;