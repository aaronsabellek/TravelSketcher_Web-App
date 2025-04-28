import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import { toast } from 'sonner';

import InputField from '@/components/Form/InputField';
import FormSubmitButton from '@/components/Buttons/FormSubmitButton';
import CancelButton from '@/components/Buttons/CancelButton';
import InputDisplay from '@/components/Form/InputDisplay';
import Form from '@/components/Form/Form';
import Container from '@/components/Container';
import { BASE_URL } from '@/utils/config';
import { useRedirectIfNotAuthenticated } from '@/hooks/authRedirects';
import { validateEmailField } from '@/utils/formValidations';

// Edit user email page
const EditEmailPage: React.FC = () => {

  // Redirect user if he is not logged in
  const { isReady } = useRedirectIfNotAuthenticated();

  const [email, setEmail] = useState('');
  const [currentEmail, setCurrentEmail] = useState('');
  const [saving, setSaving] = useState(false);
  const router = useRouter();

  // Errors
  const emailErrors = validateEmailField(email);
  const isDisabled = emailErrors.length > 0 || saving;

  // Fetch current email from user
  useEffect(() => {

    const fetchProfile = async () => {
      try {
        const res = await fetch(`${BASE_URL}/user/profile`, {
          credentials: 'include',
        });
        const data = await res.json();
        setCurrentEmail(data.email);
      } catch (err) {
        toast.error('Error loading profile.');
      }
    };

    fetchProfile();
  }, []);

  // Submit new email
  const handleSubmit = async (e: React.FormEvent) => {

    e.preventDefault();
    setSaving(true);

    if (emailErrors.length > 0) {
      emailErrors.forEach((err) => toast.error(err));
      setSaving(false);
      return;
    }

    try {
      const res = await fetch(`${BASE_URL}/user/edit_email`, {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email }),
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.error || 'Unknown error');
      }

      toast.success('Confirmation email has been sent.');
      router.push('/user/profile');

    } catch (err: any) {
      toast.error(err.message);
    } finally {
      setSaving(false);
    }
  };

  // Wait until authentication state is ready
  if (!isReady) return null;

  return (
    <Container title="Edit Email">
      <Form onSubmit={handleSubmit}>

        {/* Current email */}
        <InputDisplay label="Current email" value={currentEmail || 'Loading...'} />

        {/* New email */}
        <InputField
          label="New Email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          errors={emailErrors}
          required
        />

        {/* Button submit */}
        <FormSubmitButton
          text={saving ? 'Sending...' : 'Edit email'}
          isDisabled={isDisabled}
        />

        {/* Button cancel */}
        <CancelButton href="/user/profile" />

      </Form>
    </Container>
  );
};

export default EditEmailPage;