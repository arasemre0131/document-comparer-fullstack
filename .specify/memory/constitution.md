<!--
Sync Impact Report:
- Version: Initial → 1.0.0
- New constitution established for document-comparer-fullstack
- Added Principles: Type Safety First, API Design Excellence, User Experience Priority, Testing Discipline, Code Quality Standards
- Templates requiring updates: All validated
- Follow-up TODOs: None
-->

# Document Comparer Full-Stack Constitution

## Core Principles

### I. Type Safety First

All code MUST be strongly typed with no `any` types in production code unless explicitly justified.
- Frontend: TypeScript with strict mode enabled (`strict: true`)
- Backend: Python with type hints and mypy validation
- API contracts: Shared type definitions between frontend and backend
- Runtime validation: Pydantic models for API request/response validation

**Rationale**: Type safety prevents runtime errors, improves developer experience with autocomplete, and serves as living documentation.

### II. API Design Excellence

RESTful API design MUST follow these non-negotiable rules:
- Clear, consistent endpoint naming (`/api/v1/compare`)
- Proper HTTP methods and status codes (POST for uploads, 200/400/500)
- Request/response schemas documented with OpenAPI/Swagger
- Error responses MUST include descriptive messages and error codes
- CORS properly configured for development and production
- File size limits and validation implemented

**Rationale**: Well-designed APIs reduce integration bugs, improve debugging, and create better developer experience.

### III. User Experience Priority

UI/UX decisions MUST prioritize user productivity and accessibility:
- Keyboard navigation fully supported (arrow keys, shortcuts)
- Visual feedback for all user actions (loading states, errors, success)
- Responsive design that works on different screen sizes
- Clear error messages that guide users to resolution
- Drag-and-drop file upload with visual feedback
- Synchronized scrolling between document versions

**Rationale**: Users abandon tools that are difficult to use. Great UX is not optional.

### IV. Testing Discipline

Testing MUST cover critical paths and edge cases:
- Backend: Unit tests for diff algorithm, integration tests for API endpoints
- Frontend: Component tests for key UI interactions
- API contract tests to ensure frontend/backend compatibility
- Error handling tests for invalid inputs and edge cases
- Minimum 70% code coverage for business logic

**Rationale**: Tests prevent regressions, document expected behavior, and enable confident refactoring.

### V. Code Quality Standards

All code MUST meet these quality standards:
- Consistent formatting (Black for Python, Prettier for TypeScript)
- No linting errors (Ruff for Python, ESLint for TypeScript)
- Clear variable and function names that express intent
- Functions limited to single responsibility
- Comments for complex logic, not obvious statements
- No commented-out code in commits

**Rationale**: Consistent, clean code is easier to understand, maintain, and extend.

## Architecture Requirements

### Full-Stack Integration

- Backend serves API at `/api/v1/*` endpoints
- Frontend calls backend API, no mock data in production
- Environment-based configuration (dev/prod URLs)
- Proper error boundary implementation in React
- Backend validates all inputs before processing

### Technology Stack Compliance

**Backend**:
- Python 3.11+
- FastAPI framework
- python-difflib or diffmatchpatch library
- Pydantic for validation
- CORS middleware configured

**Frontend**:
- React 18 with TypeScript
- Vite build tool
- Tailwind CSS for styling
- Fetch API or Axios for HTTP requests
- Proper TypeScript configuration

## Development Workflow

### Quality Gates

Before any code is considered complete:
1. All linting checks pass
2. Type checking passes (mypy for Python, tsc for TypeScript)
3. Tests pass with adequate coverage
4. Manual testing of happy path and error cases
5. Code formatted consistently

### Error Handling

- Backend MUST catch and return meaningful errors
- Frontend MUST display errors to users clearly
- Network errors MUST be handled gracefully
- File validation MUST happen before processing
- Large file handling MUST be considered

## Governance

### Constitution Authority

This constitution defines the non-negotiable standards for the document comparison application. All implementation decisions MUST align with these principles.

### Amendment Process

Constitution updates require:
1. Clear justification for the change
2. Version increment following semantic versioning
3. Update to all dependent templates and documentation

### Compliance Verification

Every implementation task and code review MUST verify:
- Type safety compliance
- API design standards adherence
- User experience quality
- Test coverage adequacy
- Code quality standards

**Version**: 1.0.0 | **Ratified**: 2025-10-29 | **Last Amended**: 2025-10-29
