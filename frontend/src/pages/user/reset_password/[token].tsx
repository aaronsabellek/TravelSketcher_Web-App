import { useRouter } from 'next/router';
import { toast } from 'sonner';

import Container from '@/components/Container';
import PasswordInputGroup from '@/components/PasswordInputGroup';
import { BASE_URL } from '@/utils/config';
import { useRedirectIfNotAuthenticated } from '@/hooks/authRedirects';
import { usePasswordValidation } from '@/hooks/usePasswordValidation';

// Reset password of user
const ResetPassword = () => {

  // Redirect user if he is not logged in
  const { isReady } = useRedirectIfNotAuthenticated();

  const router = useRouter();

  // Get password validation tools from hook
  const {
    password1,
    password2,
    setPassword1,
    setPassword2,
    ruleError,
    matchError,
    isDisabled,
    saving,
    handleSubmit,
  } = usePasswordValidation({
    initialPassword1: '',
    initialPassword2: '',
  });

  // Get verification token from query
  const { token } = router.query;

  // Handle password reset
  const handleFormSubmit = async (password1: string, password2: string) => {

    const res = await fetch(`${BASE_URL}/user/reset_password/${token}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ new_password_1: password1, new_password_2: password2 }),
    });

    const data = await res.json();

    if (!res.ok) {
      throw new Error(data.error || 'Error resetting password.');
    }

    toast.success('Password changed successfully. You will be redirected...');
    setTimeout(() => router.push('/login'), 2500);
  };

  // Wait until authentication state is ready
  if (!isReady) return null;

  return (
    <Container title="Neues Passwort setzen">
      <form
        onSubmit={(e) => handleSubmit(e, handleFormSubmit)}
        className="max-w-md mx-auto space-y-4"
      >

        {/* Fake password field to prevent password autofill */}
        <input type="password" style={{ display: 'none' }} />

        {/* Password user input  */}
        <PasswordInputGroup
          password1={password1}
          password2={password2}
          setPassword1={setPassword1}
          setPassword2={setPassword2}
          ruleError={ruleError}
          matchError={matchError}
        />

        {/* Submit button */}
        <button
          type="submit"
          disabled={isDisabled}
            className={`px-5 py-2 rounded text-white transition ${
              isDisabled
              ? 'bg-gray-400 text-gray-500 cursor-not-allowed'
              : 'bg-blue-500 hover:bg-blue-600 cursor-pointer'
            }`}
        >
          {saving ? 'Saving...' : 'Save new password'}
        </button>

      </form>
    </Container>
  );
};

export default ResetPassword;