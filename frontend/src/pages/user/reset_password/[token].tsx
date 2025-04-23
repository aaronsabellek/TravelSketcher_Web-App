import { useRouter } from 'next/router';
import { useState } from 'react';
import { BASE_URL } from '../../../utils/config';
import Container from '../../../components/Container';
import { useRedirectIfNotAuthenticated } from '../../../utils/authRedirects';


const ResetPassword = () => {
  const { isReady } = useRedirectIfNotAuthenticated();

  const router = useRouter();
  const { token } = router.query;

  const [password1, setPassword1] = useState('');
  const [password2, setPassword2] = useState('');
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');
  const [saving, setSaving] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setMessage('');
    setSaving(true);

    if (password1 !== password2) {
      setError('Passwörter stimmen nicht überein.');
      setSaving(false);
      return;
    }

    try {
      const res = await fetch(`${BASE_URL}/user/reset_password/${token}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ new_password_1: password1, new_password_2: password2 }),
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.error || 'Fehler beim Zurücksetzen des Passworts.');
      }

      setMessage('Passwort erfolgreich geändert. Du wirst weitergeleitet...');
      setTimeout(() => router.push('/login'), 2500);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setSaving(false);
    }
  };

  if (!isReady) return null;

  return (
    <Container title="Neues Passwort setzen">
      <form onSubmit={handleSubmit} className="max-w-md mx-auto space-y-4">
        <label className="block">
          <span className="block text-sm font-medium">Neues Passwort</span>
          <input
            type="password"
            required
            value={password1}
            onChange={(e) => setPassword1(e.target.value)}
            className="mt-1 w-full px-3 py-2 border rounded bg-white"
          />
        </label>

        <label className="block">
          <span className="block text-sm font-medium">Passwort bestätigen</span>
          <input
            type="password"
            required
            value={password2}
            onChange={(e) => setPassword2(e.target.value)}
            className="mt-1 w-full px-3 py-2 border rounded bg-white"
          />
        </label>

        <button
          type="submit"
          disabled={saving}
          className="w-full py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          {saving ? 'Speichern...' : 'Passwort setzen'}
        </button>

        {message && <p className="text-green-600">{message}</p>}
        {error && <p className="text-red-600">{error}</p>}
      </form>
    </Container>
  );
};

export default ResetPassword;