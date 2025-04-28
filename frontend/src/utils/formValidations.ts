import {
  validateNotEmpty,
  validateUsername,
  validateEmailFormat,
  validatePasswordRules,
  validatePasswordsMatch,
  validateUrlFormat,
} from './formValidators';

// Validates input field for errors
export const validateField = (value: string, validators: ((value: string) => string | null)[]): string[] => {

  // Return errors as list
  return validators
    .map(validator => validator(value))
    .filter((error): error is string => error !== null);
};

// Validate username
export const validateUsernameField = (username: string) =>
  validateField(username, [validateNotEmpty, validateUsername]);

// Validate email
export const validateEmailField = (email: string) =>
  validateField(email, [validateNotEmpty, validateEmailFormat]);

// Validate password
export const validatePasswordField = (password: string) =>
  validateField(password, [validatePasswordRules]);

// Validate password match
export const validatePasswordMatchField = (password1: string, password2: string): string[] => {
  const matchError = validatePasswordsMatch(password1, password2);
  return matchError ? [matchError] : [];
};

// Validate city
export const validateCityField = (city: string) =>
  validateField(city, [validateNotEmpty]);

// Validate title
export const validateTitleField = (title: string) =>
  validateField(title, [validateNotEmpty]);

// Validate web link
export const validateWebLinkField = (webLink: string) =>
  validateField(webLink, [validateNotEmpty, validateUrlFormat]);