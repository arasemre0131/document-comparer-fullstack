/**
 * Main application component.
 */

import React, { useState } from 'react';
import { FileUpload } from '@/components/FileUpload';
import { DiffViewer } from '@/components/DiffViewer';
import { ErrorMessage } from '@/components/ErrorMessage';
import { compareDocuments, ApiError } from '@/services/api';
import type { ComparisonResult } from '@/types';

export const App: React.FC = () => {
  const [file1, setFile1] = useState<File | null>(null);
  const [file2, setFile2] = useState<File | null>(null);
  const [result, setResult] = useState<ComparisonResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleCompare = async () => {
    if (!file1 || !file2) {
      setError('Please upload both files before comparing');
      return;
    }

    setError(null);
    setIsLoading(true);

    try {
      const comparisonResult = await compareDocuments(file1, file2);
      setResult(comparisonResult);
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message);
      } else {
        setError('An unexpected error occurred');
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setFile1(null);
    setFile2(null);
    setResult(null);
    setError(null);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">
            Document Comparison Tool
          </h1>
          <p className="mt-2 text-sm text-gray-600">
            Upload two text documents to compare and highlight differences
          </p>
        </div>

        {error && (
          <ErrorMessage message={error} onDismiss={() => setError(null)} />
        )}

        {!result ? (
          <div className="bg-white rounded-lg shadow p-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
              <FileUpload
                label="Document 1"
                file={file1}
                onFileSelect={setFile1}
              />
              <FileUpload
                label="Document 2"
                file={file2}
                onFileSelect={setFile2}
              />
            </div>

            <div className="flex justify-center">
              <button
                onClick={handleCompare}
                disabled={!file1 || !file2 || isLoading}
                className="px-6 py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
              >
                {isLoading ? 'Comparing...' : 'Compare Documents'}
              </button>
            </div>
          </div>
        ) : (
          <div>
            <div className="mb-4 flex justify-between items-center">
              <div className="text-sm text-gray-600">
                <span className="font-medium">{result.totalChanges}</span> changes found
                {' • '}
                <span className="text-green-600">{result.additions} additions</span>
                {' • '}
                <span className="text-red-600">{result.deletions} deletions</span>
                {' • '}
                <span className="text-yellow-600">{result.modifications} modifications</span>
              </div>
              <button
                onClick={handleReset}
                className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50"
              >
                New Comparison
              </button>
            </div>
            <DiffViewer result={result} />
          </div>
        )}
      </div>
    </div>
  );
};
