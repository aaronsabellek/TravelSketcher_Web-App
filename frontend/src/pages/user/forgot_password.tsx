import { useState } from 'react';
import { toast } from 'sonner';

import { BASE_URL } from '@/utils/config';
import Container from '@/components/Container';
import { useRedirectIfAuthenticated } from '@/hooks/authRedirects';
import { isValidEmail } from '@/utils/validation';


const ForgotPassword = () => {

  // Redirect user if he is logged in
  const { isReady } = useRedirectIfAuthenticated();

  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);

  // Handle submit
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const res = await fetch(`${BASE_URL}/user/request_password_reset`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email }),
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.error || 'Fehler beim Anfordern des Links.');
      }

      toast.success(data.message);
    } catch (err: any) {
      toast.error
    } finally {
      setLoading(false);
    }
  };

  // Wait until authentication state is ready
  if (!isReady) return null;

  return (
    <Container title="Forgot password">
      <form onSubmit={handleSubmit} className="max-w-md mx-auto space-y-4">
        <div>

          {/* Email input */}
          <label className="block text-sm font-medium text-gray-700">
            Email
          </label>

          <input
            type="email"
            required
            value={email}
            pattern="[^\s@]+@[^\s@]+\.[^\s@]+"
            onChange={(e) => setEmail(e.target.value)}
            className={`
              mt-1 block w-full px-3 py-2 border rounded-md shadow-sm bg-white
              ${email && !isValidEmail(email)
                ? 'border-red-500 focus:border-red-500 focus:ring-red-500'
                : 'border-gray-300 focus:border-blue-500 focus:ring-blue-500'}
              focus:ring-1
              focus:outline-none
            `}
          />

          {/* Input condition */}
          {!isValidEmail(email) && (
            <p className="text-red-500 text-sm mt-1">
              Email has to have valid format.
            </p>
          )}

        </div>

        {/* Submit button */}
        <button
          type="submit"
          disabled={!isValidEmail(email) || loading}
          className={`w-full text-white px-5 py-2 rounded transition${
            !isValidEmail(email) || loading
              ? 'bg-gray-400 text-gray-500 cursor-not-allowed'
              : 'bg-blue-500 text-white hover:bg-blue-600 cursor-pointer'
        }`}
        >
          {loading ? 'Send link...' : 'Reset password'}
        </button>

      </form>
    </Container>
  );
};

export default ForgotPassword;