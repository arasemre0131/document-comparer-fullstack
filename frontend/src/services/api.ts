/**
 * API client for backend communication.
 */

import type { ComparisonResult, HealthResponse } from '@/types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export class ApiError extends Error {
  constructor(
    message: string,
    public statusCode: number,
    public errorCode?: string
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

/**
 * Check API health status.
 */
export async function checkHealth(): Promise<HealthResponse> {
  const response = await fetch(`${API_BASE_URL}/api/v1/health`);

  if (!response.ok) {
    throw new ApiError('Health check failed', response.status);
  }

  return response.json();
}

/**
 * Compare two documents and get differences.
 */
export async function compareDocuments(
  file1: File,
  file2: File
): Promise<ComparisonResult> {
  const formData = new FormData();
  formData.append('file1', file1);
  formData.append('file2', file2);

  const response = await fetch(`${API_BASE_URL}/api/v1/compare`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({
      detail: 'An unknown error occurred',
    }));

    throw new ApiError(
      errorData.detail || 'Comparison failed',
      response.status,
      errorData.error_code
    );
  }

  const result = await response.json();

  // Convert snake_case to camelCase
  return {
    document1Name: result.document1_name,
    document2Name: result.document2_name,
    totalChanges: result.total_changes,
    additions: result.additions,
    deletions: result.deletions,
    modifications: result.modifications,
    changes: result.changes.map((change: any) => ({
      changeType: change.change_type,
      lineNumberOld: change.line_number_old,
      lineNumberNew: change.line_number_new,
      oldContent: change.old_content,
      newContent: change.new_content,
      isModified: change.is_modified,
    })),
    comparedAt: result.compared_at,
    isIdentical: result.is_identical,
  };
}
