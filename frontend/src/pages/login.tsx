import { useState } from 'react';
import Link from 'next/link';
import { toast } from 'sonner';

import InputField from '@/components/Form/InputField';
import Button from '@/components/Buttons/Button';
import Form from '@/components/Form/Form';
import { useAuth } from '@/contexts/AuthContext';
import { useRedirectIfAuthenticated } from '@/hooks/authRedirects';
import Container from '@/components/Container';
import { BASE_URL } from '@/utils/config';

const Login = () => {
  // Redirect if user is authenticated
  const { isReady } = useRedirectIfAuthenticated();

  const [identifier, setIdentifier] = useState('');
  const [password, setPassword] = useState('');
  const { isLoading, login } = useAuth();

  const isDisabled =
    identifier.trim() === '' ||
    password.trim() === '';

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      const response = await fetch(`${BASE_URL}/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ identifier, password }),
        credentials: 'include',
      });

      if (!response.ok) {
        const data = await response.json();
        toast.error(data.error || 'Login fehlgeschlagen');
        return;
      }

      const userData = await response.json();
      login(userData);

    } catch (err) {
      toast.error('Ein Fehler ist beim Login aufgetreten.');
    }
  };

  if (isLoading) {
    return <div className="text-center mt-10">Lade Authentifizierungsstatus...</div>;
  }

  if (!isReady) return null;

  return (
    <Container title="Login">
      <Form onSubmit={handleSubmit}>

          <InputField
            label="Username or email"
            type="text"
            value={identifier}
            onChange={(e) => setIdentifier(e.target.value)}
            required
          />

          <InputField
            label="Password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />

        <Button
          text="Login"
          type="submit"
          isDisabled={isDisabled}
        />

      </Form>

      <p className="mt-4 text-sm text-center">
        Forgot password?{' '}
        <Link href="/user/forgot_password">
          <span className="text-blue-600 hover:underline cursor-pointer">Reset here</span>
        </Link>
      </p>

      <p className="mt-4 text-sm text-center">
        No verification email received?{' '}
        <Link href="/resend_verification">
          <span className="text-blue-600 hover:underline cursor-pointer">
            Send here again
          </span>
        </Link>
      </p>
    </Container>
  );
};

export default Login;