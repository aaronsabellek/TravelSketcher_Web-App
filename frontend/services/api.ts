const BASE_URL = 'http://localhost:5000';

interface LoginResponse {
  message: string;
}

export async function login(identifier: string, password: string): Promise<LoginResponse> {
  const res = await fetch(`${BASE_URL}/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: "include", // Include cookies
    body: JSON.stringify({
      identifier,
      password,
    }),
  });

  if (!res.ok) throw new Error('Login failed');

  return await res.json();
}