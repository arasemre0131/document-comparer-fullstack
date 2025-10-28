/**
 * TypeScript type definitions for the document comparison application.
 */

export enum ChangeType {
  ADD = 'add',
  DELETE = 'delete',
  MODIFY = 'modify',
}

export interface DiffChange {
  changeType: ChangeType;
  lineNumberOld: number | null;
  lineNumberNew: number | null;
  oldContent: string | null;
  newContent: string | null;
  isModified: boolean;
}

export interface ComparisonResult {
  document1Name: string;
  document2Name: string;
  totalChanges: number;
  additions: number;
  deletions: number;
  modifications: number;
  changes: DiffChange[];
  comparedAt: string;
  isIdentical: boolean;
}

export interface ErrorResponse {
  detail: string;
  error_code?: string;
}

export interface HealthResponse {
  status: string;
  version: string;
}
