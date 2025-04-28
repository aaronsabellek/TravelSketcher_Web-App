import { useState } from 'react';
import { useRouter } from 'next/router';
import { toast } from 'sonner';

import Container from '@/components/Container';
import InputField from '@/components/Form/InputField';
import FormSubmitButton from '@/components/Buttons/FormSubmitButton';
import Form from '@/components/Form/Form';
import { useRedirectIfNotAuthenticated } from '@/hooks/authRedirects';
import { BASE_URL } from '@/utils/config';
import { validatePasswordField, validatePasswordMatchField } from '@/utils/formValidations';


// Reset password of user
const ResetPassword = () => {

  // Redirect user if he is not logged in
  const { isReady } = useRedirectIfNotAuthenticated();

  const [password1, setPassword1] = useState('');
  const [password2, setPassword2] = useState('');
  const [saving, setSaving] = useState(false);

  const router = useRouter();

  // Errors
  const passwordErrors = validatePasswordField(password1);
  const passwordMatchError = validatePasswordMatchField(password1, password2);

  const allErrors = [...passwordErrors, ...passwordMatchError];
  const isDisabled = allErrors.length > 0;

  // Get verification token from query
  const { token } = router.query;

  // Handle password reset
  const handleSubmit = async (e: React.FormEvent) => {

    e.preventDefault();
    setSaving(true);

    if (allErrors.length > 0) {
      allErrors.forEach((err) => toast.error(err));
      setSaving(false);
      return;
    }

    try {
      const res = await fetch(`${BASE_URL}/user/reset_password/${token}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ new_password_1: password1, new_password_2: password2 }),
      });

      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.error || 'Error resetting password.');
      }

      toast.success('Password changed successfully. You will be redirected...');
      setTimeout(() => router.push('/login'), 2500);

    } catch (err: any) {
      toast.error(err.message || 'An unexpected error occurred.');
    } finally {
      setSaving(false)
    }
  };

  // Wait until authentication state is ready
  if (!isReady) return null;

  return (
    <Container title="Neues Passwort setzen">

      <Form onSubmit={handleSubmit}>

        {/* Fake password field to prevent password autofill */}
        <input type="password" style={{ display: 'none' }} />

        {/* New password input */}
        <InputField
            label="New password"
            type="password"
            value={password1}
            onChange={(e) => setPassword1(e.target.value)}
            errors={passwordErrors}
            required
        />

        {/* Confirm password input */}
        <InputField
            label="Confirm password"
            type="password"
            value={password2}
            onChange={(e) => setPassword2(e.target.value)}
            errors={passwordMatchError}
            required
        />

        {/* Submit button */}
        <FormSubmitButton
          text={saving ? 'Saving...' : 'Edit password'}
          isDisabled={isDisabled}
        />

      </Form>
    </Container>
  );
};

export default ResetPassword;