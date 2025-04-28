
// Sets border color of input fields dependent on error status
export const getInputBorderClass = (value: string, errors: string[]): string => {

  // Empty => grey
  if (value.trim() === '') {
    return 'border-gray-300 focus:border-gray-500 focus:ring-gray-500';
  }

  // Error => red
  if (errors.length > 0) {
    return 'border-red-500 focus:border-red-500 focus:ring-red-500';
  }

  // No error => blue
  return 'border-blue-500 focus:border-blue-500 focus:ring-blue-500';
};