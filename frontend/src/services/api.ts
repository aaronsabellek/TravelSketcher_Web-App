import { BASE_URL } from '@/utils/config';
import { toast } from 'sonner';

interface LoginResponse {
  message: string;
}

// Login
export async function login(identifier: string, password: string): Promise<LoginResponse> {
  const res = await fetch(`${BASE_URL}/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: 'include',
    body: JSON.stringify({
      identifier,
      password,
    }),
  });

  if (!res.ok) {
    const data = await res.json();
    toast.error(data.error || 'Login failed');
    throw new Error(data.error);
  }

  return await res.json();
}