
// Validate if field is not empty
export const validateNotEmpty = (value: string): string | null =>
  value.trim() === '' ? 'This field must not be empty.' : null;

// Validate if username contains no '@'
export const validateUsername = (username: string): string | null =>
  username.includes('@') ? 'Username must not contain "@".' : null;

// Validates email format
export const validateEmailFormat = (email: string): string | null =>
  /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) ? null : 'Wrong email format.';

// Validates if password matches requirements
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

// Valites if passwords match
export const validatePasswordsMatch = (pw1: string, pw2: string): string | null =>
  pw1 === pw2 ? null : 'Oasswods do not match.';

// Validate URL format
export const validateUrlFormat = (url: string): string | null => {
  url = url.trim();

  // Auto-add http:// if missing
  if (!/^https?:\/\//i.test(url)) {
    url = 'http://' + url;
  }

  // Regex to validate URL
  const urlRegex = /^(https?:\/\/)([\w.-]+\.[a-zA-Z]{2,})(:\d+)?(\/[\w./%-]*)*(\?[=&\w%-]*)?(#\w*)?$/i;

  return urlRegex.test(url) ? null : 'Invalid URL format.';
};