import React from 'react';

type ModalCancelButtonProps = {
  onClose: () => void;
};

// Cacnel button for modals (close modal instead of redirecting user)
const ModalCancelButton: React.FC<ModalCancelButtonProps> = ({ onClose }) => {
  return (
    <button
      className="px-5 py-2 text-gray-600 hover:text-black cursor-pointer"
      onClick={onClose}
    >
      Cancel
    </button>
  );
};

export default ModalCancelButton;