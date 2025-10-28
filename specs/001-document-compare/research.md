# Research: Document Comparison Tool

**Feature**: Document Comparison Tool
**Date**: 2025-10-29
**Branch**: `001-document-compare`

## Overview

This document consolidates research findings for implementing a full-stack document comparison application. Research focused on diff algorithm selection, frontend framework setup, backend API design, and performance optimization strategies.

## Technology Research

### 1. Diff Algorithm Selection

**Decision**: Use Python's built-in `difflib` library

**Rationale**:
- Ships with Python standard library (no external dependency)
- Provides multiple diff formats (unified, context, HTML)
- Well-tested and maintained
- `difflib.unified_diff()` for line-based comparison
- `difflib.SequenceMatcher` for fine-grained character-level diffs
- Adequate performance for documents up to 50,000 lines

**Alternatives Considered**:
- **diff-match-patch**: More sophisticated algorithm with better performance on large files, but adds external dependency. Chosen for simplicity as spec indicates files under 1MB.
- **GitPython**: Too heavyweight, designed for version control not simple diff
- **Custom implementation**: Unnecessary complexity, reinventing the wheel

**Implementation Notes**:
- Use `difflib.unified_diff()` for initial line-level comparison
- Use `difflib.SequenceMatcher` for inline character-level highlighting within modified lines
- Return structured JSON format with change types (add, delete, modify) and line numbers

### 2. FastAPI Setup and Best Practices

**Decision**: Standard FastAPI application with CORS middleware and file upload handling

**Rationale**:
- FastAPI provides automatic OpenAPI documentation
- Built-in Pydantic integration for request/response validation
- CORS middleware easily configured for development and production
- Native support for file uploads via `UploadFile`
- Async support for future scalability

**Best Practices Applied**:
- Use `python-multipart` for file upload handling
- Configure CORS with explicit allowed origins (not wildcard in production)
- Implement request size limits (10MB max)
- Use Pydantic models for all API request/response schemas
- Return proper HTTP status codes (200 success, 400 validation error, 500 server error)
- Structure code with clear separation: routes, models, services

**File Upload Pattern**:
```python
@app.post("/api/v1/compare")
async def compare_documents(
    file1: UploadFile,
    file2: UploadFile
) -> ComparisonResponse:
    # Validate file size
    # Validate file type (text-based)
    # Read file contents
    # Process diff
    # Return structured response
```

### 3. React + TypeScript + Vite Setup

**Decision**: Vite with React 18 and TypeScript strict mode

**Rationale**:
- Vite provides fastest dev server and build times
- React 18 hooks (useState, useEffect, useRef) sufficient for state management
- TypeScript strict mode enforces type safety (constitution requirement)
- No need for Redux/MobX - application state is simple (2 files, 1 comparison result)

**Project Initialization**:
```bash
npm create vite@latest frontend -- --template react-ts
cd frontend
npm install
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

**TypeScript Configuration**:
- Enable strict mode in `tsconfig.json`
- Use absolute imports for cleaner imports
- Define shared types in `src/types/index.ts`

### 4. Tailwind CSS Integration

**Decision**: Standard Tailwind CSS v3 with JIT mode

**Rationale**:
- Utility-first approach speeds up UI development
- JIT mode generates only used classes (smaller bundle)
- Easy to create responsive layouts
- Built-in color palette for diff highlighting

**Highlighting Colors**:
- Added lines: `bg-green-100 border-green-300`
- Deleted lines: `bg-red-100 border-red-300`
- Modified lines: `bg-yellow-100 border-yellow-300`
- Neutral/unchanged: `bg-white`

### 5. Keyboard Navigation Implementation

**Decision**: Custom React hook (`useKeyboardNav`) with event listeners

**Rationale**:
- Centralized keyboard logic in reusable hook
- Clean separation of concerns
- Easy to test in isolation
- Handles edge cases (first/last item, no differences)

**Implementation Pattern**:
```typescript
const useKeyboardNav = (differences: Diff[], scrollToRef: (index: number) => void) => {
  const [currentIndex, setCurrentIndex] = useState(0);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'ArrowDown') {
        // Navigate to next diff
      } else if (e.key === 'ArrowUp') {
        // Navigate to previous diff
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [currentIndex, differences]);

  return currentIndex;
};
```

### 6. Synchronized Scrolling

**Decision**: CSS scroll-snapping with JavaScript scroll event synchronization

**Rationale**:
- Native browser scrolling performance
- JavaScript handles sync between two panels
- Debounce scroll events to avoid infinite loops
- Maintain proportional positioning for documents of different lengths

**Implementation Pattern**:
```typescript
const useSyncScroll = (leftRef: RefObject<HTMLElement>, rightRef: RefObject<HTMLElement>) => {
  const handleScroll = (source: 'left' | 'right') => (e: Event) => {
    const sourceEl = source === 'left' ? leftRef.current : rightRef.current;
    const targetEl = source === 'left' ? rightRef.current : leftRef.current;

    if (!sourceEl || !targetEl) return;

    // Calculate proportional scroll position
    const scrollPercentage = sourceEl.scrollTop / (sourceEl.scrollHeight - sourceEl.clientHeight);
    targetEl.scrollTop = scrollPercentage * (targetEl.scrollHeight - targetEl.clientHeight);
  };
};
```

### 7. Drag and Drop File Upload

**Decision**: HTML5 Drag and Drop API with visual feedback

**Rationale**:
- Native browser support (no external library needed)
- Built-in file validation via DataTransfer API
- Easy to style with Tailwind classes
- Accessible fallback to file input

**Implementation Pattern**:
```typescript
const handleDrop = (e: DragEvent) => {
  e.preventDefault();
  const files = e.dataTransfer?.files;
  if (files && files.length > 0) {
    // Validate file type
    // Store files in state
  }
};

const handleDragOver = (e: DragEvent) => {
  e.preventDefault();
  // Show visual feedback (border highlight)
};
```

## Performance Considerations

### Backend Performance
- Use streaming for very large files (read in chunks)
- Implement timeout for diff operations (10 second max)
- Consider using `difflib.Differ` for better performance on large files
- Cache results if same file pair uploaded multiple times (future enhancement)

### Frontend Performance
- Virtualize long lists of differences (use `react-window` if >1000 diffs)
- Debounce scroll events (100ms)
- Lazy load diff viewer component
- Code split to reduce initial bundle size

## Security Considerations

### File Validation
- Check file size before processing (max 10MB)
- Validate file is text-based (check MIME type and content)
- Sanitize file names to prevent path traversal
- Limit request rate to prevent abuse

### CORS Configuration
- Development: Allow localhost origins
- Production: Whitelist specific domains only
- Never use wildcard (`*`) in production with credentials

### Input Sanitization
- Escape HTML in diff output to prevent XSS
- Validate encoding (default UTF-8, detect others)
- Handle malformed text gracefully

## Testing Strategy

### Backend Tests
- **Unit tests**: Diff service with various file pairs (identical, completely different, partial overlap)
- **Integration tests**: API endpoints with file uploads, error cases
- **Edge cases**: Empty files, very large files, binary files, malformed UTF-8

### Frontend Tests
- **Component tests**: FileUpload drag/drop, DiffViewer rendering
- **Hook tests**: Keyboard navigation, synchronized scrolling
- **Integration tests**: Full user flow (upload → compare → navigate)

### Manual Testing Checklist
- Upload two identical files → show "no differences"
- Upload files with various changes → verify highlighting colors
- Test keyboard navigation through differences
- Test synchronized scrolling
- Test drag-and-drop with invalid files
- Test on different screen sizes (responsive)
- Test on different browsers (Chrome, Firefox, Safari)

## Dependencies Summary

### Backend
```toml
[tool.poetry.dependencies]
python = "^3.11"
fastapi = "^0.109.0"
uvicorn = {extras = ["standard"], version = "^0.27.0"}
python-multipart = "^0.0.6"
pydantic = "^2.5.0"

[tool.poetry.group.dev.dependencies]
pytest = "^7.4.0"
black = "^24.1.0"
ruff = "^0.1.0"
mypy = "^1.8.0"
httpx = "^0.26.0"  # For testing FastAPI
```

### Frontend
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "@typescript-eslint/eslint-plugin": "^6.0.0",
    "@typescript-eslint/parser": "^6.0.0",
    "@vitejs/plugin-react": "^4.2.0",
    "autoprefixer": "^10.4.0",
    "eslint": "^8.56.0",
    "postcss": "^8.4.0",
    "prettier": "^3.2.0",
    "tailwindcss": "^3.4.0",
    "typescript": "^5.3.0",
    "vite": "^5.0.0",
    "vitest": "^1.2.0"
  }
}
```

## Open Questions / Future Enhancements

- Should we support comparing more than 2 documents? (Out of scope for v1)
- Should we add export functionality (PDF, HTML)? (Out of scope for v1)
- Should we persist comparison history? (Out of scope for v1)
- Should we add syntax highlighting for code files? (Out of scope for v1)
- Should we support line numbers? (Out of scope for v1)

## References

- [Python difflib documentation](https://docs.python.org/3/library/difflib.html)
- [FastAPI documentation](https://fastapi.tiangolo.com/)
- [React documentation](https://react.dev/)
- [Vite documentation](https://vitejs.dev/)
- [Tailwind CSS documentation](https://tailwindcss.com/)
