const BASE_URL = 'http://localhost:5000';

// Login
export async function login(identifier, password) {
  const res = await fetch(`${BASE_URL}/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: "include", // Include cookies
    body: JSON.stringify({
      identifier, // Username or Email
      password,
    }),
  });

  if (!res.ok) throw new Error('Login failed');

  return await res.json();
}