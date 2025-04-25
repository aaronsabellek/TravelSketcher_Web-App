import {
    validateNotEmpty,
    validateUsername,
    validateEmailFormat,
    validatePasswordRules,
    validatePasswordsMatch,
  } from './formValidators';

  export const validateField = (value: string, validators: ((value: string) => string | null)[]): string[] => {
    // Fehler sammeln und als Array zurückgeben
    return validators
      .map(validator => validator(value)) // Führe alle Validatoren aus
      .filter((error): error is string => error !== null); // Filtere null-Werte heraus
  };

  // Spezifische Felder
  export const validateUsernameField = (username: string) =>
    validateField(username, [validateNotEmpty, validateUsername]);

  export const validateEmailField = (email: string) =>
    validateField(email, [validateNotEmpty, validateEmailFormat]);

  export const validatePasswordField = (password: string) =>
    validateField(password, [validatePasswordRules]);

  export const validatePasswordMatchField = (password1: string, password2: string): string[] => {
    const matchError = validatePasswordsMatch(password1, password2);
    return matchError ? [matchError] : [];
  };

  export const validateCityField = (city: string) =>
    validateField(city, [validateNotEmpty]);

  export const validateTitleField = (title: string) =>
    validateField(title, [validateNotEmpty]);