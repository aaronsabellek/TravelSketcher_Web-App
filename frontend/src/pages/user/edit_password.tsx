import { useRouter } from 'next/router';
import Link from 'next/link';
import { toast } from 'sonner';

import Container from '@/components/Container';
import PasswordInputGroup from '@/components/PasswordInputGroup';
import { BASE_URL } from '@/utils/config';
import { useRedirectIfNotAuthenticated } from '@/hooks/authRedirects';
import { usePasswordValidation } from '@/hooks/usePasswordValidation';

// Edit password
const EditPassword = () => {

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

  // Handle password reset
  const handleFormSubmit = async (password1: string, password2: string) => {

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

    toast.success('Password edited successfully.');
    router.push('/user/profile');
  };

  // Wait until authentication state is ready
  if (!isReady) return null;

  return (
    <Container title="Edit password">
      <form
        onSubmit={(e) => handleSubmit(e, handleFormSubmit)}
        className="space-y-4 max-w-md mx-auto"
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

        {/* Buttons*/}
        <div className="flex flex-col items-center space-x-4">

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
            {saving ? 'Saving...' : 'Edit password'}
          </button>

          {/* Cancel button */}
          <Link href="/user/profile">
            <button
              type="button"
              className="px-5 py-2 cursor-pointer rounded text-red-500 hover:text-red-600"
            >
              Cancel
            </button>
          </Link>

        </div>

      </form>
    </Container>
  );
};

export default EditPassword;