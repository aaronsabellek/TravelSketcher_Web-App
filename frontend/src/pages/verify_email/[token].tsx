import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import Link from 'next/link';

// Verify emai of user with token
const EmailVerificationPage = () => {
  const router = useRouter();

  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading,] = useState(true);

  useEffect(() => {
    const { status, error } = router.query;

    if (status === 'success') {
      setMessage('Your email has been successfully confirmed!');
      setTimeout(() => router.push('/login'), 4000);
    } else if (status === 'already_verified') {
      setMessage('Your email was already confirmed.');
      setTimeout(() => router.push('/login'), 4000);
    } else if (error === 'invalid') {
      setError('Invalid or expired confirmation link.');
    } else if (error === 'notfound') {
      setError('No user found with this email.');
    }
  }, [router.query]);

  return (
    <div style={{ maxWidth: '600px', margin: '50px auto', textAlign: 'center' }}>
      {loading && <p>Verification of your email...</p>}
      {message && <p style={{ color: 'green' }}>{message}</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {!loading && (
        <p style={{ marginTop: '1rem' }}>
          You will be redirected immediately. <Link href="/login">Or click here</Link>.
        </p>
      )}
    </div>
  );
};

export default EmailVerificationPage;