import BaseButton from './BaseButton';

import { ButtonProps } from '@/types/models';

// Delete Button
const DeleteButton: React.FC<ButtonProps> = ({ text, onClick, isDisabled }) => {
  return (
    <BaseButton
      type="button"
      onClick={onClick}
      isDisabled={isDisabled}
      className={`
        ${isDisabled
            ? 'bg-gray-300 hover:bg-gray-300 text-gray-500'
            : 'cursor-pointer bg-red-500 text-white hover:bg-red-600'
        }`}
    >
      {text}
    </BaseButton>
  );
};

export default DeleteButton;