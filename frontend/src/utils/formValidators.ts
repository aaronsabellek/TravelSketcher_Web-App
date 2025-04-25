export const validateNotEmpty = (value: string): string | null =>
  value.trim() === '' ? 'This field must not be empty.' : null;

export const validateUsername = (username: string): string | null =>
  username.includes('@') ? 'Username must not contain "@".' : null;

export const validateEmailFormat = (email: string): string | null =>
  /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) ? null : 'Wrong email format.';

  // Check if password matches requirements
export function validatePasswordRules(password: string): string | null {
  if (password.length < 8) {
    return 'Password must be at least 8 characters long.';
  }

  if (!/[a-zA-Z]/.test(password)) {
    return 'Password must contain at least one letter.';
  }

  if (!/[0-9]/.test(password)) {
    return 'Password must contain at least one number.';
  }

  if (!/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
    return 'Password must contain at least one special character.';
  }

  return null;
}

export const validatePasswordsMatch = (pw1: string, pw2: string): string | null =>
  pw1 === pw2 ? null : 'Oasswods do not match.';

