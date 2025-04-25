import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import Link from 'next/link';
import { toast } from 'sonner';

import InputField from '@/components/Form/InputField';
import Button from '@/components/Buttons/Button';
import CancelButton from '@/components/Buttons/CancelButton';
import Form from '@/components/Form/Form';
import Container from '@/components/Container';
import InputDisplay from '@/components/Form/InputDisplay';
import { BASE_URL } from '@/utils/config';
import { UserProfile } from '@/types/models';
import { useRedirectIfNotAuthenticated } from '@/hooks/authRedirects';
import { validateUsernameField, validateCityField } from '@/utils/formValidations';
import { Input } from 'postcss';

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

  // Get errors
  const usernameErrors = validateUsernameField(userData.username);
  const cityErrors = validateCityField(userData.city)

  const allErrors = [
    ...usernameErrors,
    ...cityErrors,
  ];

  // Disable submit button
  const isDisabled = allErrors.length > 0;

  // Load durrent user data
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
        toast.error('Profile could not be loaded.');
      } finally {
        setLoading(false);
      }
    };

    fetchProfile();
  }, []);

  // From changes
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

      if (!res.ok) throw new Error('Error saving');

      toast.success('Profile edited successfully.')
      router.push('/user/profile');
    } catch (err) {
      toast.error('Edition failed.');
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <div>Load user data...</div>;

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
          errors={usernameErrors}
          required
        />

        {/* City */}
        <InputField
          name="city"
          label="City"
          value={userData.city}
          onChange={handleChange}
          errors={cityErrors}
          required
        />

        {/* Country */}
        <InputField
          name="country"
          label="Country"
          value={userData.country ?? ''}
          onChange={handleChange}
        />

        {/* Email (not editable here) */}
        <InputDisplay label="Email" value={userData.email} />

        {/* Link: Edit email */}
        <div>
          <Link href="/user/edit_email">
            <button className="text-blue-600 hover:underline text-sm cursor-pointer">
              Edit Email
            </button>
          </Link>
        </div>

        {/* Link: Edit password */}
        <div>
          <Link href="/user/edit_password">
            <button className="text-blue-600 hover:underline text-sm cursor-pointer">
              Edit Password
            </button>
          </Link>
        </div>

        {/* Submit button */}
        <Button
          text={saving ? 'Saving...' : 'Save changes'}
          type="submit"
          isDisabled={isDisabled}
        />

        {/* Cancel button */}
        <CancelButton href="/user/profile" />

      </Form>
    </Container>
  );
}