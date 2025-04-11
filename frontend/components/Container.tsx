import React, { ReactNode } from 'react';

interface AuthContainerProps {
  title: string;
  children: ReactNode;
}

const AuthContainer: React.FC<AuthContainerProps> = ({ title, children }) => {
  return (
    <div className="max-w-md mx-auto mt-10 p-6 border rounded-lg shadow-md border-gray-300 bg-gray-300/25">
      <h1 className="text-2xl font-bold text-center mb-4">{title}</h1>
      {children}
    </div>
  );
};

export default AuthContainer;