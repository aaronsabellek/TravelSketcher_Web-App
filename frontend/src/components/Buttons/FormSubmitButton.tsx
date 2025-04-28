import BaseButton from './BaseButton';
import { ButtonProps } from '@/types/models';

// Button for form submission
const FormSubmitButton: React.FC<ButtonProps> = ({
  text,
  onClick,
  isDisabled,
  type = 'submit',
}) => {
  return (
    <BaseButton
      type={type}
      onClick={onClick}
      isDisabled={isDisabled}
      className="mt-1 w-full bg-blue-500 text-white hover:bg-blue-600"
    >
      {text}
    </BaseButton>
  );
};

export default FormSubmitButton;