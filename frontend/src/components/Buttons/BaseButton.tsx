import React from 'react';

import { ButtonProps } from '@/types/models';

// Base Button for Button, FormSubmitButton and DeleteButton
const BaseButton: React.FC<ButtonProps> = ({
    children,
    onClick,
    type = 'button',
    isDisabled = false,
    className = '',
  }) => {
    const disabledStyle = 'bg-gray-300 hover:bg-gray-300 text-gray-500';

    return (
      <button
        type={type}
        disabled={isDisabled}
        onClick={onClick}
        className={`
          py-2 px-4 rounded-lg
          ${className}
          ${isDisabled ? disabledStyle : 'cursor-pointer'}
        `}
      >
        {children}
      </button>
    );
  };

export default BaseButton;