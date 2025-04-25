import { useState } from 'react';
import { useRouter } from 'next/router';
import Link from 'next/link';
import { toast } from 'sonner';

import Container from '@/components/Container';
import InputField from '@/components/Form/InputField';
import Button from '@/components/Buttons/Button';
import CancelButton from '@/components/Buttons/CancelButton';
import Form from '@/components/Form/Form';
import { BASE_URL } from '@/utils/config';
import { validatePasswordField, validatePasswordMatchField } from '@/utils/formValidations';
import { useRedirectIfNotAuthenticated } from '@/hooks/authRedirects';

// Edit password
const EditPassword = () => {

  // Redirect user if he is not logged in
  const { isReady } = useRedirectIfNotAuthenticated();

  const [password1, setPassword1] = useState('');
  const [password2, setPassword2] = useState('');
  const [saving, setSaving] = useState(false);

  const router = useRouter();

  const passwordErrors = validatePasswordField(password1);
  const passwordMatchError = validatePasswordMatchField(password1, password2);

  const allErrors = [...passwordErrors, ...passwordMatchError];

  const isDisabled = allErrors.length > 0;

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
      const res = await fetch(`${BASE_URL}/user/edit_password`, {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ new_password_1: password1, new_password_2: password2 }),
      });

      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.error || 'Error editing password.');
      }

      toast.success('Password edited successfully!');
      router.push('/user/profile');

    } catch (err: any) {
      toast.error(err.message || 'An unexpected error occurred.');
    } finally {
      setSaving(false)
    }
  };

  // Wait until authentication state is ready
  if (!isReady) return null;

  return (
    <Container title="Edit password">
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
        <Button
          text={saving ? 'Saving...' : 'Edit password'}
          type="submit"
          isDisabled={isDisabled}
        />

        {/* Cancel button */}
        <CancelButton href="/user/profile" />

      </Form>
    </Container>
  );
};

export default EditPassword;