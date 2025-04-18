import { useState } from 'react';
import { useRedirectIfAuthenticated } from '../utils/authRedirects';
import Container from '../components/Container';
import { BASE_URL } from '../utils/config';

const ResendVerification = () => {
    const [email, setEmail] = useState('');
    const [message, setMessage] = useState('');
    const [error, setError] = useState('');

    // Redirect if user is authenticated
    useRedirectIfAuthenticated();

    const handleSubmit = async (e: React.FormEvent) => {
      e.preventDefault();
      setMessage('');
      setError('');

      try {
        const response = await fetch(`${BASE_URL}/resend_verification`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ email }),
          credentials: 'include', // Hier wird das Cookie für die Session mitgeschickt
        });

        const data = await response.json();

        if (!response.ok) {
          setError(data.error || 'An error occurred while resending the verification email.');
        } else {
          setMessage(data.message || 'An unexpected error occurred.');
        }
      } catch (err) {
        console.error(err);
        setError('An error occurred. Please try again later.');
      }
    };

    return (
      <Container title="Resend Verification Email">
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label
              className="block text-sm font-medium text-gray-700"
              htmlFor="email"
            >
              Email Address
            </label>
            <input
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm bg-white"
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <button
            type="submit"
            className="w-full py-2 px-4 bg-blue-500 text-white font-semibold rounded-lg hover:bg-blue-600"
          >
            Resend Verification
          </button>
        </form>

        {message && <p className="success-message">{message}</p>}
        {error && <p className="error-message">{error}</p>}
     </Container>
    );
  };

  export default ResendVerification;