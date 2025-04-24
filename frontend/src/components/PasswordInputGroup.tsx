import React from 'react';

interface PasswordInputGroupProps {
  password1: string;
  password2: string;
  setPassword1: (val: string) => void;
  setPassword2: (val: string) => void;
  ruleError: string | null;
  matchError: string | null;
}

const PasswordInputGroup: React.FC<PasswordInputGroupProps> = ({
  password1,
  password2,
  setPassword1,
  setPassword2,
  ruleError,
  matchError,
}) => {

  // Set red borders for errors
  const getInputBorderClass = (input: string, error: string | null) => {
    if (input.trim() === '') return 'border-gray-300 focus:border-blue-500 focus:ring-blue-500'; // Neutral if input is empty
    if (error) return 'border-red-500 focus:border-red-500 focus:ring-red-500'; // Show red border if there's an error
    return 'border-gray-300 focus:border-blue-500 focus:ring-blue-500';
  };

  return (
    <>

      {/* New password input */}
      <div>
        <label className="block text-sm font-medium text-gray-700">
          New password
        </label>
        <input
          type="password"
          value={password1}
          onChange={(e) => setPassword1(e.target.value)}
          className={`mt-1 block w-full px-3 py-2 border focus:ring-1 focus:outline-none rounded-md shadow-sm bg-white ${getInputBorderClass(password1, ruleError)}`}
          required
        />

        {/* Error note */}
        {ruleError && password1.trim() !== '' && <p className="text-red-500 text-sm">{ruleError}</p>}
      </div>

      {/* Confirm password input */}
      <div>
        <label className="block text-sm font-medium text-gray-700">
          Confirm password
        </label>
        <input
          type="password"
          value={password2}
          onChange={(e) => setPassword2(e.target.value)}
          className={`mt-1 block w-full px-3 py-2 border focus:ring-1 focus:outline-none rounded-md shadow-sm bg-white ${getInputBorderClass(password2, matchError)}`}
          required
        />

        {/* Error note */}
        {matchError && password2.trim() !== '' && <p className="text-red-500 text-sm">{matchError}</p>}
      </div>

      {/* Note about conditions of password */}
      <div>
        <p>The password has to have at least 8 characters long and must contain at least one letter, one number and one special character.</p>
      </div>
    </>
  );
};

export default PasswordInputGroup;