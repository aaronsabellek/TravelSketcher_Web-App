// Check if email has proper format
export const isValidEmail = (email: string) =>
    /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);

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

// Check if two passwords match
export function validatePasswordMatch(pw1: string, pw2: string): string | null {
    return pw1 === pw2 ? null : 'Passwords do not match.';
}