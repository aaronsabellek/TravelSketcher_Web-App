import React from 'react';

type ButtonProps = {
  text: string;
  isDisabled?: boolean;
  type?: 'button' | 'submit' | 'reset'; // Optional: Falls du den Button-Typ anpassen möchtest
  onClick?: () => void;
};

// Main button used on website
const Button: React.FC<ButtonProps> = ({ text, isDisabled, type = 'submit', onClick }) => {
  return (
    <button
      type={type}
      disabled={isDisabled}
      onClick={onClick}
      className={`w-full py-2 px-4 rounded-lg cursor-pointer ${
        isDisabled
          ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
          : 'bg-blue-500 text-white hover:bg-blue-600'
      }`}
    >
      {text}
    </button>
  );
};

export default Button;