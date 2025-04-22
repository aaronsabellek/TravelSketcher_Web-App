import { useState } from 'react';
import { BASE_URL } from '../../utils/config';
import Container from '../../components/Container';

const ForgotPassword = () => {
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  // Check for valid email format
  const isValidEmail = (email: string) =>
    /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setMessage('');
    setError('');
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

      setMessage(data.message);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container title="Forgot password">
      <form onSubmit={handleSubmit} className="max-w-md mx-auto space-y-4">
        <label className="block text-sm font-medium text-gray-700">
          E-Mail-Adresse
          <input
            type="email"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="mt-1 w-full px-3 py-2 border rounded border-gray-300 bg-white"
          />
        </label>
        <button
          type="submit"
          disabled={!isValidEmail(email) || loading}
          className={`w-full bg-blue-600 text-white px-5 py-2 rounded hover:bg-blue-700 transition${
            !isValidEmail(email) || loading
            ? 'bg-gray-300 text-gray-500 opacity-50 cursor-not-allowed'
            : 'bg-blue-500 text-white hover:bg-blue-600 cursor-pointer'
        }`}
        >
          {loading ? 'Send link...' : 'Reset password'}
        </button>

        {message && <p className="text-green-600">{message}</p>}
        {error && <p className="text-red-600">{error}</p>}
      </form>
    </Container>
  );
};

export default ForgotPassword;