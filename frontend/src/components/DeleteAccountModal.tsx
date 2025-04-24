import { useState } from 'react';
import { toast } from 'sonner';

import { BASE_URL } from '@/utils/config';
import { useAuth } from '@/contexts/AuthContext';

interface Props {
  isOpen: boolean;
  onClose: () => void;
  onDeleted: () => void;
}

// Administers deletion of user account
const DeleteAccountModal: React.FC<Props> = ({ isOpen, onClose, onDeleted }) => {

  const [password, setPassword] = useState('');
  const [deleting, setDeleting] = useState(false);

  const { setIsLoggedIn } = useAuth();

  if (!isOpen) return null;

  // Handle delition of user account
  const handleDelete = async () => {

    // Check for password
    if (!password) return toast.error('Please enter password');

    setDeleting(true);
    try {
      const res = await fetch(`${BASE_URL}/user/delete`, {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ password }),
      });

      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.error || 'Error while deleting');
      }

      toast.success('Deleted account successfully');

      await fetch(`${BASE_URL}/logout`, {
        method: 'POST',
        credentials: 'include',
      });

      setIsLoggedIn(false);
      onDeleted();
    } catch (err: any) {
      toast.error(err.message || 'Deleting account failed');
    } finally {
      setDeleting(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black/30 z-50 flex items-center justify-center">
      <div className="bg-white p-6 rounded-lg shadow-lg w-[90%] max-w-md">
        <h2 className="text-lg font-semibold text-red-600 mb-4">Delete account?</h2>

        <p className="text-sm mb-4 text-gray-700">
            Your data will be deleted permanently.
        </p>

        <p className="text-sm mb-4 text-gray-700">
          Please enter your password to confirm the deletion of your account.
        </p>

        {/* Fake password field to prevent password autofill */}
        <input type="password" style={{ display: 'none' }} />

        {/* Input field for apssword */}
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
          className="w-full border rounded px-3 py-2 text-sm mb-4"
        />

        <div className="flex justify-end space-x-3">

          {/* Cancel button */}
          <button
            onClick={onClose}
            className="text-gray-600 hover:text-black text-sm cursor-pointer"
          >
            Cancel
          </button>

          {/* Delete button */}
          <button
            onClick={handleDelete}
            disabled={deleting}
            className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded text-sm cursor-pointer"
          >
            {deleting ? 'Deleting...' : 'Delete'}
          </button>

        </div>
      </div>
    </div>
  );
};

export default DeleteAccountModal;