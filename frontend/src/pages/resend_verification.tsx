import { useState } from 'react';
import { toast } from 'sonner';

import Container from '@/components/Container';
import InputField from '@/components/Form/InputField';
import Button from '@/components/Buttons/Button';
import { useRedirectIfAuthenticated } from '@/hooks/authRedirects';
import { validateEmailField } from '@/utils/formValidations';
import { BASE_URL } from '@/utils/config';

const ResendVerification = () => {
  // Redirect if user is authenticated
  const { isReady } = useRedirectIfAuthenticated();

  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);

  const emailErrors = validateEmailField(email);

  const isDisabled = emailErrors.length > 0;

  const handleSubmit = async (e: React.FormEvent) => {

    e.preventDefault();
    setLoading(true);

    try {
      const response = await fetch(`${BASE_URL}/resend_verification`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email }),
        credentials: 'include',
      });

      const data = await response.json();

      if (!response.ok) {
        toast.error(data.error || 'An error occurred while resending the verification email.');
      } else {
        toast.success(data.message || 'Verification email has been sent successfully.');
      }
      } catch (err: any) {
        toast.error(err.message || 'An error occurred. Please try again later.');
        setLoading(false)
      }
    };

    if (!isReady) return null;

    return (
      <Container title="Resend Verification Email">
        <form onSubmit={handleSubmit} className="space-y-4 max-w-md mx-auto">

          <InputField
            label="Email address"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            errors={emailErrors}
            required
          />

          <Button
            text='Resend verification'
            type="submit"
            isDisabled={isDisabled}
          />

        </form>
     </Container>
    );
  };

  export default ResendVerification;