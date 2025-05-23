import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import Link from 'next/link';
import { toast } from 'sonner';

import InputField from '@/components/Form/InputField';
import FormSubmitButton from '@/components/Buttons/FormSubmitButton';
import CancelButton from '@/components/Buttons/CancelButton';
import Form from '@/components/Form/Form';
import Container from '@/components/Container';
import InputDisplay from '@/components/Form/InputDisplay';
import { BASE_URL } from '@/utils/config';
import { UserProfile } from '@/types/models';
import { useRedirectIfNotAuthenticated } from '@/hooks/authRedirects';
import { validateUsernameField, validateCityField } from '@/utils/formValidations';

// Edit user profile
export default function EditUserProfile() {

  const { isReady } = useRedirectIfNotAuthenticated();
  const router = useRouter();

  const [userData, setUserData] = useState<Pick<UserProfile, 'username' | 'email' |'city' | 'country'>>({
    username: '',
    email: '',
    city: '',
    country: '',
  });

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  // Errors
  const usernameErrors = validateUsernameField(userData.username);
  const cityErrors = validateCityField(userData.city)

  const allErrors = [
    ...usernameErrors,
    ...cityErrors,
  ];

  const isDisabled = allErrors.length > 0;

  // Load current user data
  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const res = await fetch(`${BASE_URL}/user/profile`, {
          credentials: 'include',
        });

        if (!res.ok) throw new Error('Error loading profile');

        const data = await res.json();
        setUserData({
          username: data.username || '',
          email: data.email,
          city: data.city || '',
          country: data.country || '',
        });
      } catch (err) {
        console.log(err)
        toast.error('Profile could not be loaded.');
      } finally {
        setLoading(false);
      }
    };

    fetchProfile();
  }, []);

  // Handle changes
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setUserData({ ...userData, [e.target.name]: e.target.value });
  };

  // Submit changes
  const handleSubmit = async (e: React.FormEvent) => {

    e.preventDefault();
    setSaving(true);

    if (allErrors.length > 0) {
      allErrors.forEach((err) => toast.error(err));
      return;
    }

    try {
      const res = await fetch(`${BASE_URL}/user/edit`, {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(userData),
      });

      const data = await res.json();

      if (!res.ok) {
        toast.error(data.error || 'Error saving.');
        return
      }

      toast.success('Profile edited successfully.')
      router.push('/user/profile');

    } catch (err) {
      console.log(err)
      toast.error('An unexpected error occurred.');
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <div>Load user data...</div>;

  // Wait until authentication state is ready
  if (!isReady) return null;

  return (
    <Container title="Edit profile">
      <Form onSubmit={handleSubmit}>

        {/* Username */}
        <InputField
          name="username"
          label="Username"
          value={userData.username}
          onChange={handleChange}
          maxLength={50}
          errors={usernameErrors}
          required
        />

        {/* City */}
        <InputField
          name="city"
          label="City"
          value={userData.city}
          onChange={handleChange}
          maxLength={50}
          errors={cityErrors}
          required
        />

        {/* Country */}
        <InputField
          name="country"
          label="Country"
          maxLength={50}
          value={userData.country ?? ''}
          onChange={handleChange}
        />

        {/* Email (not editable here) */}
        <InputDisplay label="Email" value={userData.email} />

        {/* Link: Edit email */}
        <div>
          <Link href="/user/edit_email">
            <button className="paragraph_link text-sm">
              Edit Email
            </button>
          </Link>
        </div>

        {/* Link: Edit password */}
        <div>
          <Link href="/user/edit_password">
            <button className="paragraph_link text-sm">
              Edit Password
            </button>
          </Link>
        </div>

        {/* Submit button */}
        <FormSubmitButton
          text={saving ? 'Saving...' : 'Save changes'}
          isDisabled={isDisabled}
        />

        {/* Cancel button */}
        <CancelButton href="/user/profile" />

      </Form>
    </Container>
  );
}