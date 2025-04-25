export const getValidationErrors = (value: string, validators: ((v: string) => string | null)[]): string[] =>
    validators
      .map(fn => fn(value))
      .filter((e): e is string => e !== null);