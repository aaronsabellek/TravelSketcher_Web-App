import { useState } from 'react';
import { useRouter } from 'next/router';
import { useRedirectIfAuthenticated } from '../utils/authRedirects';
import Link from 'next/link';
import BASE_URL from '../utils/config';

const Register = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [city, setCity] = useState('');
  const [longitude, setLongitude] = useState('');
  const [latitude, setLatitude] = useState('');
  const [country, setCountry] = useState('');
  const [currency, setCurrency] = useState('');
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');
  const router = useRouter();

  // Redirect if user is authenticated
  useRedirectIfAuthenticated();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setMessage('');

    const data = { username, email, password, city, longitude, latitude, country, currency };

    try {
      const response = await fetch(`${BASE_URL}/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });

      const result = await response.json();

      if (response.ok) {
        setMessage(result.message);
        setTimeout(() => {
          router.push('/login');
        }, 2000);
      } else {
        setError(result.error || 'Etwas ist schiefgegangen.');
      }
    } catch (err) {
      console.error(err);
      setError('Ein Fehler ist beim Senden der Anfrage aufgetreten.');
    }
  };

  return (
    <div className="max-w-md mx-auto mt-10 p-6 border rounded-lg shadow-md bg-white">
      <h1 className="text-2xl font-bold text-center mb-4">Registrierung</h1>
      <form onSubmit={handleSubmit}>
        {[
          { label: 'Benutzername', id: 'username', value: username, setValue: setUsername },
          { label: 'Email', id: 'email', value: email, setValue: setEmail },
          { label: 'Passwort', id: 'password', value: password, setValue: setPassword, type: 'password' },
          { label: 'Stadt', id: 'city', value: city, setValue: setCity },
          { label: 'Longitude', id: 'longitude', value: longitude, setValue: setLongitude },
          { label: 'Latitude', id: 'latitude', value: latitude, setValue: setLatitude },
          { label: 'Land', id: 'country', value: country, setValue: setCountry },
          { label: 'Währung', id: 'currency', value: currency, setValue: setCurrency },
        ].map(({ label, id, value, setValue, type = 'text' }) => (
          <div className="mb-4" key={id}>
            <label htmlFor={id} className="block text-sm font-medium text-gray-700">{label}</label>
            <input
              type={type}
              id={id}
              value={value}
              onChange={(e) => setValue(e.target.value)}
              required
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm"
            />
          </div>
        ))}

        <button
          type="submit"
          className="w-full py-2 px-4 bg-green-500 text-white font-semibold rounded-lg hover:bg-green-600"
        >
          Registrieren
        </button>
      </form>
      <p className="mt-4 text-sm text-center">
        Keine Verifizierungs-E-Mail erhalten?{' '}
        <Link href="/resend_verification">
          <span className="text-blue-600 underline cursor-pointer">
            Hier erneut senden
          </span>
        </Link>
      </p>
      {error && <p className="text-red-500 mt-4 text-center">{error}</p>}
      {message && <p className="text-green-500 mt-4 text-center">{message}</p>}
    </div>
  );
};

export default Register;