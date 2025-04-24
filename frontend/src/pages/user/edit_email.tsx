import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import { toast } from 'sonner';

import Container from '@/components/Container';
import { BASE_URL } from '@/utils/config';
import { useRedirectIfNotAuthenticated } from '@/hooks/authRedirects';
import { isValidEmail } from '@/utils/validation';

// Edit user email page
const EditEmailPage: React.FC = () => {

  // Redirect user if he is not logged in
  const { isReady } = useRedirectIfNotAuthenticated();

  const [email, setEmail] = useState('');
  const [currentEmail, setCurrentEmail] = useState('');
  const [saving, setSaving] = useState(false);
  const router = useRouter();

  // Fetch current email from user
  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const res = await fetch(`${BASE_URL}/user/profile`, {
          credentials: 'include',
        });
        const data = await res.json();
        setCurrentEmail(data.email);
      } catch (err) {
        toast.error('Error loading profile.');
      }
    };

    fetchProfile();
  }, []);

  // Submit new email
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);

    try {
      const res = await fetch(`${BASE_URL}/user/edit_email`, {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email }),
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.error || 'Unknown error');
      }

      toast.success('Confirmation email has been sent.');
      router.push('/user/profile');
    } catch (err: any) {
      toast.error(err.message);
    } finally {
      setSaving(false);
    }
  };

  // Wait until authentication state is ready
  if (!isReady) return null;

  return (
    <Container title="Edit Email">
      <form onSubmit={handleSubmit} className="space-y-4 max-w-md mx-auto">

        {/* Current email */}
        <div>
          <label className="block text-sm font-medium text-gray-700">
            Current email
          </label>
          <p className="text-gray-600 mt-1 px-3 py-2 border border-gray-300 rounded-md bg-gray-100">
            {currentEmail || 'Loading...'}
          </p>
        </div>

        {/* New email */}
        <div>
          <label className="block text-sm font-medium text-gray-700">
            New email
          </label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            pattern="[^\s@]+@[^\s@]+\.[^\s@]+"
            className={`
              mt-1 block w-full px-3 py-2 border rounded-md shadow-sm bg-white
              ${email && !isValidEmail(email)
                ? 'border-red-500 focus:border-red-500 focus:ring-red-500'
                : 'border-gray-300 focus:border-blue-500 focus:ring-blue-500'}
              focus:ring-1
              focus:outline-none
            `}
          />

          {/* input condition */}
          {!isValidEmail(email) && (
            <p className="text-red-500 text-sm mt-1">
              Email has to have valid format.
            </p>
          )}

        </div>

        {/* Button submit */}
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
            {saving ? 'Sending...' : 'Edit email'}
          </button>

          {/* Button cancel */}
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