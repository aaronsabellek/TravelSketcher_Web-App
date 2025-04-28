import { useState } from 'react';
import Link from 'next/link';
import { toast } from 'sonner';

import InputField from '@/components/Form/InputField';
import FormSubmitButton from '@/components/Buttons/FormSubmitButton';
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

  // Disable button when field is empty
  const isDisabled =
    identifier.trim() === '' ||
    password.trim() === '';

  // Handle submit
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
        toast.error(data.error || 'Login failed');
        return;
      }

      const userData = await response.json();
      login(userData);

    } catch (err) {
      toast.error('An error occurred during login.');
    }
  };

  if (isLoading) {
    return <div className="text-center mt-10">Loading authentication status...</div>;
  }

  // Wait until authentication state is ready
  if (!isReady) return null;

  return (
    <Container title="Login">
      <Form onSubmit={handleSubmit}>

          {/* Identifier */}
          <InputField
            label="Username or email"
            type="text"
            value={identifier}
            onChange={(e) => setIdentifier(e.target.value)}
            required
          />

          {/* Password */}
          <InputField
            label="Password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />

        {/* Submit button */}
        <FormSubmitButton
          text="Login"
          isDisabled={isDisabled}
        />

      </Form>

      {/* Links */}
      <p className="form-paragraph">
        Forgot password?{' '}
        <Link href="/user/forgot_password">
          <span className="paragraph_link">Reset password here</span>
        </Link>
      </p>

      <p className="form-paragraph">
        No verification email received?{' '}
        <Link href="/resend_verification">
          <span className="paragraph_link">
            Send here again
          </span>
        </Link>
      </p>

    </Container>
  );
};

export default Login;