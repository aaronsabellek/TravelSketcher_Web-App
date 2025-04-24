import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import Link from 'next/link';

import Container from '@/components/Container';
import DeleteAccountModal from '@/components/DeleteAccountModal';
import { useRedirectIfNotAuthenticated } from '@/hooks/authRedirects';
import { BASE_URL } from '@/utils/config';
import { UserProfile } from '@/types/models';

const Profile: React.FC = () => {
  const { isReady } = useRedirectIfNotAuthenticated();

  const [user, setUser] = useState<UserProfile | null>(null);
  const [error, setError] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(true);
  const router = useRouter();

  // State for delete modal
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
          setError(err?.error || 'Error retrieving profile');
        } else {
          const data = await res.json();
          setUser(data);
        }
      } catch (err) {
        setError('Server error or no response received.');
      } finally {
        setLoading(false);
      }
    };

    fetchUserProfile();
  }, [router]);

  // Loading / Error
  if (loading) return <div>Loading profile...</div>;
  if (error) return <div style={{ color: 'red' }}>Error: {error}</div>;
  if (!user) return <div>No user found.</div>;

  if (!isReady) return null;

  // Show profile data
  return (
    <Container title="User profile">

          {/* Username */}
          <div className="mb-4">
            <label htmlFor="identifier" className="block text-sm font-medium text-gray-700">Username</label>
            <p className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm">{user.username}</p>
          </div>

          {/* City */}
          <div className="mb-4">
            <label htmlFor="identifier" className="block text-sm font-medium text-gray-700">City</label>
            <p className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm">{user.city}</p>
          </div>

          {/* Country */}
          {user.country && (
          <div className="mb-4">
            <label htmlFor="identifier" className="block text-sm font-medium text-gray-700">Country</label>
            <p className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm">{user.country}</p>
          </div>
          )}

          {/* Email */}
          <div className="mb-4">
            <label htmlFor="identifier" className="block text-sm font-medium text-gray-700">Email</label>
            <p className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm">{user.email}</p>
          </div>

          {/* Buttons */}
          <div className="pt-4 flex flex-col items-center space-y-3">
            <Link href="/user/edit">
              <button className="bg-blue-600 hover:bg-blue-700 text-white px-5 py-2 rounded-lg transition-all cursor-pointer">
                Edit profile
              </button>
            </Link>

            <button
              onClick={() => setShowDeleteModal(true)}
              className="text-red-600 hover:underline text-sm cursor-pointer"
            >
              Delete account
            </button>
          </div>

      <DeleteAccountModal
        isOpen={showDeleteModal}
        onClose={() => setShowDeleteModal(false)}
        onDeleted={() => router.push('/about')}
      />
    </Container>
  );
};

export default Profile;