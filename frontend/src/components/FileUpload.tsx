/**
 * File upload component with click-to-browse functionality.
 */

import React, { useRef } from 'react';

interface FileUploadProps {
  label: string;
  file: File | null;
  onFileSelect: (file: File | null) => void;
}

export const FileUpload: React.FC<FileUploadProps> = ({
  label,
  file,
  onFileSelect,
}) => {
  const inputRef = useRef<HTMLInputElement>(null);

  const handleClick = () => {
    inputRef.current?.click();
  };

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;
    if (files && files.length > 0) {
      onFileSelect(files[0]!);
    }
  };

  const handleRemove = (event: React.MouseEvent) => {
    event.stopPropagation();
    onFileSelect(null);
    if (inputRef.current) {
      inputRef.current.value = '';
    }
  };

  return (
    <div>
      <label className="block text-sm font-medium text-gray-700 mb-2">
        {label}
      </label>
      <div
        onClick={handleClick}
        className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center cursor-pointer hover:border-blue-500 hover:bg-blue-50 transition-colors"
      >
        <input
          ref={inputRef}
          type="file"
          onChange={handleFileChange}
          className="hidden"
          accept=".txt,.md,.py,.js,.ts,.jsx,.tsx,.json,.yaml,.yml,.xml,.html,.css,.scss,.java,.c,.cpp,.h,.hpp,.rs,.go,.rb,.php,.sh,.bash,.sql,.pdf"
        />

        {file ? (
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <svg
                className="h-5 w-5 text-gray-400"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                />
              </svg>
              <span className="text-sm font-medium text-gray-900 truncate">
                {file.name}
              </span>
              <span className="text-xs text-gray-500">
                ({(file.size / 1024).toFixed(1)} KB)
              </span>
            </div>
            <button
              onClick={handleRemove}
              className="ml-2 p-1 text-red-500 hover:text-red-700 rounded hover:bg-red-50"
            >
              <svg
                className="h-5 w-5"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </button>
          </div>
        ) : (
          <div>
            <svg
              className="mx-auto h-12 w-12 text-gray-400"
              stroke="currentColor"
              fill="none"
              viewBox="0 0 48 48"
            >
              <path
                d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
                strokeWidth={2}
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
            <p className="mt-2 text-sm text-gray-600">
              Click to browse or drag and drop
            </p>
            <p className="mt-1 text-xs text-gray-500">
              Text files or PDF (max 10MB, max 10 pages for PDF)
            </p>
          </div>
        )}
      </div>
    </div>
  );
};
