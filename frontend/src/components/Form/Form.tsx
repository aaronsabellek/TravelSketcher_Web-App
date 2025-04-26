import React from 'react';

type FormProps = {
  onSubmit: (e: React.FormEvent) => void;
  children: React.ReactNode;
  className?: string;
};

// Standard form
const Form: React.FC<FormProps> = ({ onSubmit, children, className = '' }) => {
  return (
    <form onSubmit={onSubmit} className={`space-y-4 max-w-md mx-auto ${className}`}>
      {children}
    </form>
  );
};

export default Form;