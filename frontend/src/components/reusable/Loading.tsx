import React from 'react';

const Loading = ({message}:{message:string}) => {
  return (
    <div className="fixed top-0 left-0 min-h-screen w-screen flex items-center justify-center bg-gray-900/80">
      <div className="flex flex-col items-center space-y-4">
        <div className="w-10 h-10 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
        <p className="text-gray-700 dark:text-gray-300 text-sm font-medium">{message}</p>
      </div>
    </div>
  );
};

export default Loading;
