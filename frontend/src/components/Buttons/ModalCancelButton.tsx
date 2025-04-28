import React from 'react';

import { ButtonProps } from '@/types/models';

// Cancel button for modals (close modal instead of redirecting user)
const ModalCancelButton: React.FC<ButtonProps> = ({ onClose }) => {
  return (
    <button
      className="px-5 py-2 text-gray-600 hover:text-black cursor-pointer"
      onClick={onClose}
      type="button"
    >
      Cancel
    </button>
  );
};

export default ModalCancelButton;