import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';

const EmailVerificationPage = () => {
  const router = useRouter();

  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const { status, error } = router.query;

    if (status === 'success') {
      setMessage('Deine E-Mail wurde erfolgreich bestätigt!');
      setTimeout(() => router.push('/login'), 4000);
    } else if (status === 'already_verified') {
      setMessage('Deine E-Mail war bereits bestätigt.');
      setTimeout(() => router.push('/login'), 4000);
    } else if (error === 'invalid') {
      setError('Ungültiger oder abgelaufener Bestätigungslink.');
    } else if (error === 'notfound') {
      setError('Kein Benutzer mit dieser E-Mail gefunden.');
    }
  }, [router.query]);

  return (
    <div style={{ maxWidth: '600px', margin: '50px auto', textAlign: 'center' }}>
      {loading && <p>Verifiziere deine E-Mail...</p>}
      {message && <p style={{ color: 'green' }}>{message}</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {!loading && (
        <p style={{ marginTop: '1rem' }}>
          Du wirst gleich weitergeleitet. <a href="/login">Oder hier klicken</a>.
        </p>
      )}
    </div>
  );
};

export default EmailVerificationPage;