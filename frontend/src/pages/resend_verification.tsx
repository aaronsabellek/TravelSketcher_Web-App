import { useState } from 'react';
import { useRouter } from 'next/router';
import { toast } from 'sonner';

import Container from '@/components/Container';
import InputField from '@/components/Form/InputField';
import Button from '@/components/Buttons/FormSubmitButton';
import { useRedirectIfAuthenticated } from '@/hooks/authRedirects';
import { validateEmailField } from '@/utils/formValidations';
import { BASE_URL } from '@/utils/config';

const ResendVerification = () => {

  // Redirect if user is authenticated
  const { isReady } = useRedirectIfAuthenticated();

  const router = useRouter();

  const [email, setEmail] = useState('');
  const [, setLoading] = useState(false);

  // Errors
  const emailErrors = validateEmailField(email);
  const isDisabled = emailErrors.length > 0;

  // Handle subnmit
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
        setTimeout(() => {
          router.push('/login');
        }, 2000);
      }

      } catch (err) {
        console.log(err)
        toast.error('An error occurred. Please try again later.');
        setLoading(false)
      }
    };

    // Wait until authentication state is ready
    if (!isReady) return null;

    return (
      <Container title="Resend Verification Email">
        <form onSubmit={handleSubmit} className="space-y-4 max-w-md mx-auto">

          {/* Email */}
          <InputField
            label="Email"
            type="email"
            value={email}
            maxLength={50}
            onChange={(e) => setEmail(e.target.value)}
            errors={emailErrors}
            required
          />

          {/* Submit button */}
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