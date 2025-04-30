import { useState } from 'react';
import { useRouter } from 'next/router';
import Link from 'next/link';
import { toast } from 'sonner';

import InputField from '@/components/Form/InputField';
import FormSubmitButton from '@/components/Buttons/FormSubmitButton';
import Container from '@/components/Container';
import Form from '@/components/Form/Form';
import { useRedirectIfAuthenticated } from '@/hooks/authRedirects';
import { BASE_URL } from '@/utils/config';
import { validateUsernameField, validateEmailField, validatePasswordField, validateCityField } from '@/utils/formValidations';

const Register = () => {

  // Redirect if user is authenticated
  const { isReady } = useRedirectIfAuthenticated();

  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [city, setCity] = useState('');
  const [country, setCountry] = useState('');

  const router = useRouter();

  // Errors
  const usernameErrors = validateUsernameField(username);
  const emailErrors = validateEmailField(email);
  const passwordErrors = validatePasswordField(password);
  const cityErrors = validateCityField(city)

  const allErrors = [
    ...usernameErrors,
    ...emailErrors,
    ...passwordErrors,
    ...cityErrors,
  ];

  // Disable submit button
  const isDisabled = allErrors.length > 0;

  // Handle submit
  const handleFormSubmit = async (e: React.FormEvent) => {

    e.preventDefault();

    if (allErrors.length > 0) {
      allErrors.forEach((err) => toast.error(err));
      return;
    }

    const data = { username, email, password, city, country: country || '' };

    try {
      const response = await fetch(`${BASE_URL}/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });

      const result = await response.json();

      if (response.ok) {
        toast.success(result.message || 'Registration successful!');
        setTimeout(() => {
          router.push('/login');
        }, 2000);

      } else {
        toast.error(result.error || 'Something went wrong.');
      }

    } catch (err) {
      console.log(err)
      toast.error('An error occurred while sending the request.');
    }
  };

  if (!isReady) return null;

  return (
    <Container title="Register">
      <Form onSubmit={handleFormSubmit}>

        {/* Username */}
        <InputField
          label="Username"
          type="text"
          value={username}
          maxLength={20}
          onChange={(e) => setUsername(e.target.value)}
          errors={usernameErrors}
          required
        />

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

        {/* Password */}
        <InputField
          label="Password"
          type="password"
          value={password}
          maxLength={50}
          onChange={(e) => setPassword(e.target.value)}
          errors={passwordErrors}
          required
        />

        {/* City */}
        <InputField
          label="City"
          type="text"
          value={city}
          maxLength={50}
          onChange={(e) => setCity(e.target.value)}
          required
        />

        {/* Country*/}
        <InputField
          label="Country"
          type="text"
          value={country}
          maxLength={50}
          onChange={(e) => setCountry(e.target.value)}
        />

        {/* Submit button */}
        <FormSubmitButton
          text="Register"
          isDisabled={isDisabled}
        />

      </Form>

      {/* Link */}
      <p className="form-paragraph -mt-2">
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

export default Register;