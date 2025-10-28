# Data Model: Document Comparison Tool

**Feature**: Document Comparison Tool
**Date**: 2025-10-29
**Branch**: `001-document-compare`

## Overview

This document defines the data structures used throughout the document comparison application. All models are technology-agnostic but include implementation notes for Python (Pydantic) and TypeScript.

## Core Entities

### 1. Document

Represents a single text file uploaded by the user.

**Attributes**:
- `filename`: String - Original name of the uploaded file
- `content`: String - Full text content of the document
- `size_bytes`: Integer - File size in bytes
- `encoding`: String - Text encoding (default: UTF-8)
- `line_count`: Integer - Total number of lines in the document

**Validation Rules**:
- `filename` must not be empty
- `size_bytes` must not exceed 10,485,760 (10MB)
- `encoding` must be valid encoding name (UTF-8, ASCII, ISO-8859-1, etc.)
- `content` must be valid text (not binary data)

**Python Implementation**:
```python
from pydantic import BaseModel, Field, validator

class Document(BaseModel):
    filename: str = Field(..., min_length=1, max_length=255)
    content: str
    size_bytes: int = Field(..., ge=0, le=10_485_760)
    encoding: str = Field(default="utf-8")
    line_count: int = Field(..., ge=0)

    @validator('encoding')
    def validate_encoding(cls, v):
        # Validate encoding is supported
        return v
```

**TypeScript Implementation**:
```typescript
interface Document {
  filename: string;
  content: string;
  sizeBytes: number;
  encoding: string;
  lineCount: number;
}
```

### 2. DiffChange

Represents a single change (addition, deletion, or modification) between two documents.

**Attributes**:
- `change_type`: Enum (ADD, DELETE, MODIFY) - Type of change
- `line_number_old`: Integer | null - Line number in original document (null for additions)
- `line_number_new`: Integer | null - Line number in new document (null for deletions)
- `old_content`: String | null - Original text (null for additions)
- `new_content`: String | null - New text (null for deletions)
- `is_modified`: Boolean - True if line was modified (not pure add/delete)

**Validation Rules**:
- `change_type` must be one of: ADD, DELETE, MODIFY
- For ADD: `old_content` must be null, `new_content` must be present
- For DELETE: `new_content` must be null, `old_content` must be present
- For MODIFY: both `old_content` and `new_content` must be present

**Python Implementation**:
```python
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, validator

class ChangeType(str, Enum):
    ADD = "add"
    DELETE = "delete"
    MODIFY = "modify"

class DiffChange(BaseModel):
    change_type: ChangeType
    line_number_old: Optional[int] = None
    line_number_new: Optional[int] = None
    old_content: Optional[str] = None
    new_content: Optional[str] = None
    is_modified: bool = False

    @validator('old_content')
    def validate_old_content(cls, v, values):
        if values.get('change_type') == ChangeType.ADD and v is not None:
            raise ValueError('old_content must be null for ADD')
        if values.get('change_type') == ChangeType.DELETE and v is None:
            raise ValueError('old_content must be present for DELETE')
        return v

    @validator('new_content')
    def validate_new_content(cls, v, values):
        if values.get('change_type') == ChangeType.DELETE and v is not None:
            raise ValueError('new_content must be null for DELETE')
        if values.get('change_type') == ChangeType.ADD and v is None:
            raise ValueError('new_content must be present for ADD')
        return v
```

**TypeScript Implementation**:
```typescript
enum ChangeType {
  ADD = 'add',
  DELETE = 'delete',
  MODIFY = 'modify'
}

interface DiffChange {
  changeType: ChangeType;
  lineNumberOld: number | null;
  lineNumberNew: number | null;
  oldContent: string | null;
  newContent: string | null;
  isModified: boolean;
}
```

### 3. ComparisonResult

Contains the complete result of comparing two documents.

**Attributes**:
- `document1_name`: String - Filename of first document
- `document2_name`: String - Filename of second document
- `total_changes`: Integer - Total number of differences found
- `additions`: Integer - Count of added lines
- `deletions`: Integer - Count of deleted lines
- `modifications`: Integer - Count of modified lines
- `changes`: Array<DiffChange> - List of all changes
- `compared_at`: DateTime - Timestamp when comparison was performed
- `is_identical`: Boolean - True if documents are identical

**Validation Rules**:
- `total_changes` must equal `additions + deletions + modifications`
- `changes` array length must equal `total_changes`
- `is_identical` must be true if `total_changes == 0`

**Python Implementation**:
```python
from datetime import datetime
from typing import List
from pydantic import BaseModel, Field, validator

class ComparisonResult(BaseModel):
    document1_name: str
    document2_name: str
    total_changes: int = Field(..., ge=0)
    additions: int = Field(..., ge=0)
    deletions: int = Field(..., ge=0)
    modifications: int = Field(..., ge=0)
    changes: List[DiffChange]
    compared_at: datetime = Field(default_factory=datetime.utcnow)
    is_identical: bool

    @validator('total_changes')
    def validate_total_changes(cls, v, values):
        expected = values.get('additions', 0) + values.get('deletions', 0) + values.get('modifications', 0)
        if v != expected:
            raise ValueError(f'total_changes must equal additions + deletions + modifications')
        return v

    @validator('is_identical')
    def validate_is_identical(cls, v, values):
        if values.get('total_changes', -1) == 0 and not v:
            raise ValueError('is_identical must be true when total_changes is 0')
        return v
```

**TypeScript Implementation**:
```typescript
interface ComparisonResult {
  document1Name: string;
  document2Name: string;
  totalChanges: number;
  additions: number;
  deletions: number;
  modifications: number;
  changes: DiffChange[];
  comparedAt: string; // ISO 8601 datetime
  isIdentical: boolean;
}
```

## API Request/Response Models

### POST /api/v1/compare

**Request**: Multipart form data
- `file1`: File (required) - First document to compare
- `file2`: File (required) - Second document to compare

**Success Response** (200 OK):
```json
{
  "document1_name": "version1.txt",
  "document2_name": "version2.txt",
  "total_changes": 5,
  "additions": 2,
  "deletions": 1,
  "modifications": 2,
  "changes": [
    {
      "change_type": "add",
      "line_number_old": null,
      "line_number_new": 3,
      "old_content": null,
      "new_content": "This is a new line",
      "is_modified": false
    },
    {
      "change_type": "delete",
      "line_number_old": 5,
      "line_number_new": null,
      "old_content": "This line was removed",
      "new_content": null,
      "is_modified": false
    },
    {
      "change_type": "modify",
      "line_number_old": 8,
      "line_number_new": 7,
      "old_content": "Hello World",
      "new_content": "Hello Beautiful World",
      "is_modified": true
    }
  ],
  "compared_at": "2025-10-29T10:30:00Z",
  "is_identical": false
}
```

**Error Response** (400 Bad Request):
```json
{
  "detail": "File size exceeds maximum limit of 10MB",
  "error_code": "FILE_TOO_LARGE"
}
```

**Error Response** (400 Bad Request):
```json
{
  "detail": "File must be a text document, binary files not supported",
  "error_code": "INVALID_FILE_TYPE"
}
```

**Error Response** (500 Internal Server Error):
```json
{
  "detail": "An error occurred while comparing documents",
  "error_code": "COMPARISON_FAILED"
}
```

### GET /api/v1/health

**Success Response** (200 OK):
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

## Error Codes

Standard error codes returned by the API:

- `FILE_TOO_LARGE`: File exceeds 10MB size limit
- `INVALID_FILE_TYPE`: File is not a text document
- `MISSING_FILE`: Required file not provided in request
- `ENCODING_ERROR`: Unable to decode file with detected encoding
- `COMPARISON_FAILED`: Unexpected error during diff processing
- `TIMEOUT_ERROR`: Comparison took longer than 10 seconds

## State Transitions

### Document Upload Flow

```
[No files] → User drags file → [Dragging over drop zone]
                              ↓
                         [File validated]
                              ↓
                    [One file uploaded] → User uploads second file
                              ↓
                    [Two files ready] → User clicks compare
                              ↓
                    [Comparing...] → Backend processes
                              ↓
                    [Results displayed]
```

### Comparison State Machine

```
IDLE → UPLOADING → VALIDATING → COMPARING → SUCCESS | ERROR
  ↑                                            ↓         ↓
  └────────────────────────────────────────────┴─────────┘
                    (Reset/New Comparison)
```

## Index and Lookup Requirements

No database persistence required for v1. All data exists in memory during the comparison session.

**Future Enhancements** (Out of scope for v1):
- Add database to store comparison history
- Index by user_id for multi-user support
- Add full-text search on comparison results
- Cache recent comparisons by file hash

## Data Flow Diagram

```
User Browser                  Backend API                 Diff Service
     │                             │                           │
     ├─── POST /api/v1/compare ───→│                           │
     │    (file1, file2)            │                           │
     │                              ├─── Validate files ───────→│
     │                              │                           │
     │                              │←── Validation OK ─────────┤
     │                              │                           │
     │                              ├─── Perform diff ─────────→│
     │                              │                           │
     │                              │←── DiffChange[] ──────────┤
     │                              │                           │
     │←── ComparisonResult ─────────┤                           │
     │    (JSON)                    │                           │
     │                              │                           │
```

## Naming Conventions

### Python (Backend)
- Classes: PascalCase (e.g., `ComparisonResult`)
- Functions/methods: snake_case (e.g., `compare_documents`)
- Constants: UPPER_SNAKE_CASE (e.g., `MAX_FILE_SIZE`)
- Module names: snake_case (e.g., `diff_service.py`)

### TypeScript (Frontend)
- Interfaces/Types: PascalCase (e.g., `ComparisonResult`)
- Functions/variables: camelCase (e.g., `compareDocuments`)
- Constants: UPPER_SNAKE_CASE (e.g., `MAX_FILE_SIZE`)
- Components: PascalCase (e.g., `DiffViewer`)

### API Endpoints
- Lowercase with hyphens (e.g., `/api/v1/compare`)
- Versioned (v1, v2, etc.)
- RESTful naming conventions
