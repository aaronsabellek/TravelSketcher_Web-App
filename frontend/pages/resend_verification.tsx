import { useState } from 'react';
import { useRedirectIfAuthenticated } from '../utils/authRedirects';
import BASE_URL from '../utils/config';

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
      <div className="max-w-md mx-auto mt-10 p-6 border rounded-lg shadow-md border-gray-300 bg-gray-300/25">
        <h1 className="text-2xl font-bold text-center mb-4">Resend Verification Email</h1>
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
            className="w-full py-2 px-4 bg-blue-500 text-white font-semibold rounded-lg hover:bg-green-600"
          >
            Resend Verification
          </button>
        </form>

        {message && <p className="success-message">{message}</p>}
        {error && <p className="error-message">{error}</p>}
        {/*
        <style jsx>{`
          .resend-verification-container {
            max-width: 400px;
            margin: 0 auto;
            padding: 1rem;
            background-color: #f9f9f9;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
          }

          h1 {
            font-size: 24px;
            margin-bottom: 1rem;
            text-align: center;
          }

          form {
            display: flex;
            flex-direction: column;
            gap: 1rem;
          }

          label {
            font-size: 16px;
          }

          input {
            padding: 0.5rem;
            font-size: 16px;
            border: 1px solid #ccc;
            border-radius: 4px;
          }

          button {
            background-color: #007bff;
            color: white;
            padding: 0.75rem;
            font-size: 16px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
          }

          button:hover {
            background-color: #0056b3;
          }

          .success-message {
            color: green;
            text-align: center;
            margin-top: 1rem;
          }

          .error-message {
            color: red;
            text-align: center;
            margin-top: 1rem;
          }
        `}</style>
        */}
      </div>
    );
  };

  export default ResendVerification;