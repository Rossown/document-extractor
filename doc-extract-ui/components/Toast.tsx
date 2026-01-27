import React, { useEffect } from 'react';

interface ToastProps {
  message: string;
  type?: 'success' | 'error' | 'info';
  show: boolean;
  onClose: () => void;
  link?: { href: string; label?: string };
}

const toastStyles: Record<string, string> = {
  base: 'fixed top-5 right-5 z-50 min-w-[200px] px-4 py-3 rounded shadow-lg flex items-center transition-all duration-300',
  success: 'bg-green-500 text-white',
  error: 'bg-red-500 text-white',
  info: 'bg-blue-500 text-white',
};

const Toast: React.FC<ToastProps> = ({ message, type = 'info', show, onClose, link }) => {
  useEffect(() => {
    if (show) {
      const timer = setTimeout(onClose, 10000);
      return () => clearTimeout(timer);
    }
  }, [show, onClose]);

  if (!show) return null;

  return (
    <div className={`${toastStyles.base} ${toastStyles[type]}`}
         role="alert">
      <span className="mr-2">
        {type === 'success' && '✔️'}
        {type === 'error' && '❌'}
        {type === 'info' && 'ℹ️'}
      </span>
      <span>{message}</span>
      {link && (
        <a
          href={link.href}
          className="ml-4 underline text-white font-semibold hover:text-gray-200 transition"
          target="_blank"
          rel="noopener noreferrer"
        >
          {link.label || 'View'}
        </a>
      )}
      <button
        className="ml-4 text-white font-bold"
        onClick={onClose}
        aria-label="Close"
      >
        ×
      </button>
    </div>
  );
};

export default Toast;
