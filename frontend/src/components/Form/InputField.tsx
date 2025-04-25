import React from 'react';
import { getInputBorderClass } from '@/styles/getInputBorderClass'; // Importiere die Funktion

type InputFieldProps = {
  label: string;
  type?: string;
  value: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  name?: string;
  errors?: string[];
  required?: boolean;
  placeholder?: string;
};

const InputField: React.FC<InputFieldProps> = ({
  label,
  type = 'text',
  value,
  onChange,
  name,
  errors = [],
  required = false,
  placeholder = '',
}) => {
  // Berechnung der Klassen für den Rand
  const inputBorderClass = getInputBorderClass(value, errors);

  return (
    <div>
      <label className="block text-sm font-medium text-gray-700">
        {label} {required && <span className="text-red-500">*</span>}
      </label>
      <input
        name={name}
        type={type}
        value={value}
        onChange={onChange}
        required={required}
        placeholder={placeholder}
        className={`mt-1 block w-full px-3 py-2 border focus:ring-1 focus:outline-none rounded-md shadow-sm bg-white ${inputBorderClass}`}
      />
      {required && value && errors.length > 0 && (
        <div>
          {errors.map((error, idx) => (
            <p key={idx} className="text-red-500 text-sm">
              {error}
            </p>
          ))}
        </div>
      )}
    </div>
  );
};

export default InputField;