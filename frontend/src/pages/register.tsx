import { useState } from 'react';
import { useRouter } from 'next/router';
import { useRedirectIfAuthenticated } from '../utils/authRedirects';
import Container from '../components/Container';
import Link from 'next/link';
import { BASE_URL } from '../utils/config';
import { toast } from 'sonner';

const Register = () => {
  // Redirect if user is authenticated
  const { isReady } = useRedirectIfAuthenticated();

  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [city, setCity] = useState('');
  const [country, setCountry] = useState('');

  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const data = { username, email, password, city, country };

    try {
      const response = await fetch(`${BASE_URL}/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });

      const result = await response.json();

      if (response.ok) {
        toast.success(result.message || 'Registrierung erfolgreich!');
        setTimeout(() => {
          router.push('/login');
        }, 2000);
      } else {
        toast.error(result.error || 'Etwas ist schiefgegangen.');
      }
    } catch (err) {
      toast.error('Ein Fehler ist beim Senden der Anfrage aufgetreten.');
    }
  };

  if (!isReady) return null;

  return (
    <Container title="Register">
      <form onSubmit={handleSubmit}>
        {[
          { label: 'Username', id: 'username', value: username, setValue: setUsername, required: true },
          { label: 'Email', id: 'email', value: email, setValue: setEmail, required: true },
          { label: 'Password', id: 'password', value: password, setValue: setPassword, type: 'password', required: true },
          { label: 'City', id: 'city', value: city, setValue: setCity, required: true },
          { label: 'Country', id: 'country', value: country, setValue: setCountry },
        ].map(({ label, id, value, setValue, type = 'text', required }) => (
          <div className="mb-4" key={id}>
            <label htmlFor={id} className="block text-sm font-medium text-gray-700">
              {label}
              {required && (
                <>
                  {" "}
                  (<span className="text-red-500">*</span>required)
                </>
              )}
            </label>
            <input
              type={type}
              id={id}
              value={value}
              onChange={(e) => setValue(e.target.value)}
              required
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm bg-white"
            />
          </div>
        ))}

        <button
          type="submit"
          className="w-full py-2 px-4 bg-blue-500 text-white font-semibold rounded-lg cursor-pointer hover:bg-blue-600"
        >
          Register
        </button>
      </form>

      <p className="mt-2 text-sm text-center">
        Forgot password?{' '}
        <Link href="/user/forgot_password">
          <span className="text-blue-600 underline cursor-pointer">Reset here</span>
        </Link>
      </p>

      <p className="mt-4 text-sm text-center">
      No verification email received?{' '}
        <Link href="/resend_verification">
          <span className="text-blue-600 underline cursor-pointer">
          Send here again
          </span>
        </Link>
      </p>
    </Container>
  );
};

export default Register;