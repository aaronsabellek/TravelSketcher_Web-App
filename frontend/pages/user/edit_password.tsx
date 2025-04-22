import { useState } from 'react';
import { useRouter } from 'next/router';
import Link from 'next/link';
import { BASE_URL } from '../../utils/config';
import { toast } from 'sonner';
import Container from '../../components/Container';

const EditPassword = () => {
  const router = useRouter();
  const [password1, setPassword1] = useState('');
  const [password2, setPassword2] = useState('');
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setError(null);

    if (password1 !== password2) {
      setError('Passwords do not match.');
      setSaving(false);
      return;
    }

    try {
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
    } catch (err: any) {
      setError(err.message);
      toast.error(err.message);
    } finally {
      setSaving(false);
    }
  };

  const isDisabled = saving || password1.trim() === '' || password2.trim() === '' || password1 !== password2;

  return (
    <Container title="Edit password">
      <form onSubmit={handleSubmit} className="space-y-4 max-w-md mx-auto">
        {error && <p className="text-red-600">{error}</p>}

        {/* Fake password field to prevent password autofill */}
        <input type="password" style={{ display: 'none' }} />

        <div>
          <label className="block text-sm font-medium text-gray-700">New password</label>
          <input
            type="password"
            name="new_password_1"
            value={password1}
            onChange={(e) => setPassword1(e.target.value)}
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm bg-white"
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">Confirm password</label>
          <input
            type="password"
            name="new_password_2"
            value={password2}
            onChange={(e) => setPassword2(e.target.value)}
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm bg-white"
            required
          />
        </div>

        <div>
            <p>The password has to have at least 8 characters long and must contain at least one letter, one number and one special character.</p>
        </div>

        <div className="flex flex-col items-center space-x-4">
          <button
            type="submit"
            disabled={isDisabled}
            className={`px-5 py-2 rounded text-white transition ${
              isDisabled
              ? 'bg-gray-400 text-gray-500 cursor-not-allowed'
              : 'bg-blue-500 hover:bg-blue-600'
            }`}
          >
            {saving ? 'Speichern...' : 'Edit password'}
          </button>

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