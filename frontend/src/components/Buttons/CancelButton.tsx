import Link from 'next/link';

import { ButtonProps } from '@/types/models';

// Main button used for canceling an action and go to another page
const CancelButton: React.FC<ButtonProps> = ({ href = '', className = '' }) => {
  return (
    <div className={`flex justify-center ${className}`}>
      <Link href={href}>
        <p className="px-5 text-gray-600 hover:text-black cursor-pointer">
          Cancel
        </p>
      </Link>
    </div>
  );
};

export default CancelButton;