import React from 'react';

interface InputDisplayProps {
  label: string;
  value: string;
}

const InputDisplay: React.FC<InputDisplayProps> = ({ label, value }) => {
  return (
    <div className="mb-4">
      <label htmlFor={label.toLowerCase()} className="block text-sm font-medium text-gray-700">
        {label}
      </label>
      <p className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm">
        {value}
      </p>
    </div>
  );
};

export default InputDisplay;