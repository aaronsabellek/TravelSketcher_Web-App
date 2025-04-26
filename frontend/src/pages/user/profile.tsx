import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import Link from 'next/link';
import { toast } from 'sonner';

import Container from '@/components/Container';
import Button from '@/components/Buttons/Button';
import InputDisplay from '@/components/Form/InputDisplay';
import DeleteAccountModal from '@/components/DeleteAccountModal';
import { useRedirectIfNotAuthenticated } from '@/hooks/authRedirects';
import { BASE_URL } from '@/utils/config';
import { UserProfile } from '@/types/models';

// Show profile data of user
const Profile: React.FC = () => {
  const { isReady } = useRedirectIfNotAuthenticated();

  const [user, setUser] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const router = useRouter();

  const [showDeleteModal, setShowDeleteModal] = useState(false);


  // Fetch user profile
  useEffect(() => {
    const fetchUserProfile = async () => {

      try {
        const res = await fetch(`${BASE_URL}/user/profile`, {
          credentials: 'include',
        });

        if (!res.ok) {
          const err = await res.json();
          toast.error(err?.error || 'Error retrieving profile');
        } else {
          const data = await res.json();
          setUser(data);
        }
      } catch (err) {
        toast.error('Server error or no response received.');
      } finally {
        setLoading(false);
      }
    };

    fetchUserProfile();
  }, [router]);

  // Loading / Error
  if (loading) return <div>Loading profile...</div>;
  if (!user) return <div>No user found.</div>;

  // Wait until authentication state is ready
  if (!isReady) return null;

  // Show profile data
  return (
    <Container title="User profile">

          {/* Username */}
          <InputDisplay label="Username" value={user.username} />

          {/* City */}
          <InputDisplay label="City" value={user.city} />

          {/* Country */}
          {user.country && (
            <InputDisplay label="Country" value={user.country} />
          )}

          {/* Email */}
          <InputDisplay label="Email" value={user.email} />

          {/* Buttons */}
          <Link href="/user/edit">
            <Button
              text="Edit profile"
              type="button"
              isDisabled={false}
            />
          </Link>

          <button
            onClick={() => setShowDeleteModal(true)}
            className="text-red-600 mt-3 hover:underline text-sm cursor-pointer mx-auto block"
          >
            Delete account
          </button>

      <DeleteAccountModal
        isOpen={showDeleteModal}
        onClose={() => setShowDeleteModal(false)}
        onDeleted={() => router.push('/about')}
      />
    </Container>
  );
};

export default Profile;