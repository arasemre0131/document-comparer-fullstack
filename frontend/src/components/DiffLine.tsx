/**
 * Single diff line component with highlighting.
 */

import React from 'react';
import { ChangeType, type DiffChange } from '@/types';

interface DiffLineProps {
  change: DiffChange;
}

export const DiffLine: React.FC<DiffLineProps> = ({ change }) => {
  const getBackgroundColor = () => {
    switch (change.changeType) {
      case ChangeType.ADD:
        return 'bg-diff-add-100 border-l-4 border-diff-add-300';
      case ChangeType.DELETE:
        return 'bg-diff-delete-100 border-l-4 border-diff-delete-300';
      case ChangeType.MODIFY:
        return 'bg-diff-modify-100 border-l-4 border-diff-modify-300';
      default:
        return 'bg-white';
    }
  };

  const getChangeIcon = () => {
    switch (change.changeType) {
      case ChangeType.ADD:
        return <span className="text-diff-add-300 font-bold">+</span>;
      case ChangeType.DELETE:
        return <span className="text-diff-delete-300 font-bold">-</span>;
      case ChangeType.MODIFY:
        return <span className="text-diff-modify-300 font-bold">~</span>;
      default:
        return null;
    }
  };

  return (
    <div className={`p-2 font-mono text-sm ${getBackgroundColor()}`}>
      <div className="flex items-start space-x-2">
        <span className="flex-shrink-0 w-6 text-center">{getChangeIcon()}</span>
        <div className="flex-1 grid grid-cols-2 gap-4">
          {/* Old content */}
          <div className="min-h-[1.5rem]">
            {change.oldContent !== null && (
              <div>
                <span className="text-xs text-gray-500 mr-2">
                  L{change.lineNumberOld}
                </span>
                <span className={change.changeType === ChangeType.DELETE ? 'line-through' : ''}>
                  {change.oldContent || <span className="text-gray-400 italic">empty line</span>}
                </span>
              </div>
            )}
          </div>

          {/* New content */}
          <div className="min-h-[1.5rem]">
            {change.newContent !== null && (
              <div>
                <span className="text-xs text-gray-500 mr-2">
                  L{change.lineNumberNew}
                </span>
                <span>
                  {change.newContent || <span className="text-gray-400 italic">empty line</span>}
                </span>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
