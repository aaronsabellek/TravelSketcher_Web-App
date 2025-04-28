import { useState } from 'react';
import { toast } from 'sonner';

import Container from '@/components/Container';
import InputField from '@/components/Form/InputField';
import FormSubmitButton from '@/components/Buttons/FormSubmitButton';
import Form from '@/components/Form/Form';
import { useRedirectIfAuthenticated } from '@/hooks/authRedirects';
import { BASE_URL } from '@/utils/config';
import { validateEmailField } from '@/utils/formValidations';

const ForgotPassword = () => {

  // Redirect user if he is logged in
  const { isReady } = useRedirectIfAuthenticated();

  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);

  // Errors
  const emailErrors = validateEmailField(email);
  const isDisabled = emailErrors.length > 0 || loading;

  // Handle submit
  const handleSubmit = async (e: React.FormEvent) => {

    e.preventDefault();
    setLoading(true);

    if (emailErrors.length > 0) {
      emailErrors.forEach((err) => toast.error(err));
      return;
    }

    try {
      const res = await fetch(`${BASE_URL}/user/request_password_reset`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email }),
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.error || 'Error requesting link.');
      }

      toast.success(data.message);
    } catch (err: any) {
      toast.error(err)
    } finally {
      setLoading(false);
    }
  };

  // Wait until authentication state is ready
  if (!isReady) return null;

  return (
    <Container title="Forgot password">
      <Form onSubmit={handleSubmit}>

        {/* Email input */}
        <InputField
          label="New Email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          errors={emailErrors}
          required
        />

        {/* Submit button */}
        <FormSubmitButton
          text={loading ? 'Send link...' : 'Reset password'}
          isDisabled={isDisabled}
        />

      </Form>
    </Container>
  );
};

export default ForgotPassword;