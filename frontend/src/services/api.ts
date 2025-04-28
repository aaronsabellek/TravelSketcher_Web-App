import { BASE_URL } from '@/utils/config';

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

  if (!res.ok) throw new Error('Login failed');

  return await res.json();
}