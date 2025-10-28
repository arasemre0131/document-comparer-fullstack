/**
 * Side-by-side diff viewer component.
 */

import React from 'react';
import { DiffLine } from './DiffLine';
import type { ComparisonResult } from '@/types';

interface DiffViewerProps {
  result: ComparisonResult;
}

export const DiffViewer: React.FC<DiffViewerProps> = ({ result }) => {
  if (result.isIdentical) {
    return (
      <div className="bg-white rounded-lg shadow p-8 text-center">
        <svg
          className="mx-auto h-16 w-16 text-green-500"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
          />
        </svg>
        <h3 className="mt-4 text-lg font-medium text-gray-900">
          Documents are identical
        </h3>
        <p className="mt-2 text-sm text-gray-600">
          No differences found between {result.document1Name} and {result.document2Name}
        </p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow overflow-hidden">
      {/* Header */}
      <div className="bg-gray-50 border-b border-gray-200 p-4">
        <div className="grid grid-cols-2 gap-4 font-medium text-sm text-gray-700">
          <div className="flex items-center space-x-2">
            <svg
              className="h-4 w-4 text-gray-400"
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
            <span>{result.document1Name}</span>
          </div>
          <div className="flex items-center space-x-2">
            <svg
              className="h-4 w-4 text-gray-400"
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
            <span>{result.document2Name}</span>
          </div>
        </div>
      </div>

      {/* Diff content */}
      <div className="max-h-[600px] overflow-auto">
        {result.changes.length === 0 ? (
          <div className="p-8 text-center text-gray-500">
            No changes detected
          </div>
        ) : (
          <div className="divide-y divide-gray-200">
            {result.changes.map((change, index) => (
              <DiffLine key={index} change={change} />
            ))}
          </div>
        )}
      </div>

      {/* Legend */}
      <div className="bg-gray-50 border-t border-gray-200 p-4">
        <div className="flex items-center justify-center space-x-6 text-xs text-gray-600">
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 bg-diff-add-100 border border-diff-add-300 rounded"></div>
            <span>Added</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 bg-diff-delete-100 border border-diff-delete-300 rounded"></div>
            <span>Deleted</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 bg-diff-modify-100 border border-diff-modify-300 rounded"></div>
            <span>Modified</span>
          </div>
        </div>
      </div>
    </div>
  );
};
