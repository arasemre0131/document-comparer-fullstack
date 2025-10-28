# Document Comparison Tool

A full-stack web application for comparing two versions of text documents with visual highlighting of differences.

## Features

- **Visual Diff Highlighting**: See additions (green), deletions (red), and modifications (yellow) at a glance
- **Side-by-Side View**: Compare documents in a clean, organized layout
- **Drag & Drop Upload**: Quick file upload with visual feedback
- **Keyboard Navigation**: Navigate through differences using arrow keys
- **Synchronized Scrolling**: Both document panels scroll together to maintain context
- **Type-Safe**: Full TypeScript frontend and Python type hints backend
- **RESTful API**: Clean API design with OpenAPI documentation

## Tech Stack

### Backend
- Python 3.11+
- FastAPI
- Pydantic for validation
- difflib for document comparison
- pytest for testing

### Frontend
- React 18
- TypeScript (strict mode)
- Vite
- Tailwind CSS
- Vitest for testing

## Quick Start

### Prerequisites

- Python 3.11 or higher
- Node.js 18 or higher
- Poetry (recommended) or pip

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd document-comparer-fullstack
   ```

2. **Setup Backend**
   ```bash
   cd backend
   poetry install  # or: pip install -r requirements.txt
   ```

3. **Setup Frontend**
   ```bash
   cd frontend
   npm install
   ```

### Running the Application

1. **Start the backend server** (in `backend/` directory):
   ```bash
   poetry run uvicorn src.main:app --reload --port 8000
   ```

   The API will be available at http://localhost:8000
   - API docs: http://localhost:8000/docs
   - Health check: http://localhost:8000/api/v1/health

2. **Start the frontend dev server** (in `frontend/` directory):
   ```bash
   npm run dev
   ```

   The application will be available at http://localhost:5173

### Running Tests

**Backend:**
```bash
cd backend
poetry run pytest
poetry run pytest --cov=src  # with coverage
```

**Frontend:**
```bash
cd frontend
npm test
```

## Usage

1. Open http://localhost:5173 in your browser
2. Upload two text files using the upload areas
3. Click "Compare Documents"
4. View the highlighted differences:
   - Green: Lines added in the second document
   - Red: Lines deleted from the first document
   - Yellow: Lines modified between documents
5. Use arrow keys (↑↓) to navigate through changes
6. Scroll either panel to see synchronized scrolling

## Project Structure

```
document-comparer-fullstack/
├── backend/                 # Python FastAPI backend
│   ├── src/
│   │   ├── api/            # API routes and models
│   │   ├── services/       # Business logic
│   │   └── utils/          # Utilities
│   └── tests/              # Backend tests
├── frontend/               # React TypeScript frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── hooks/         # Custom React hooks
│   │   ├── services/      # API client
│   │   ├── types/         # TypeScript definitions
│   │   └── styles/        # CSS styles
│   └── tests/             # Frontend tests
└── specs/                 # Spec Kit documentation
    └── 001-document-compare/
        ├── spec.md        # Feature specification
        ├── plan.md        # Technical plan
        ├── tasks.md       # Implementation tasks
        ├── data-model.md  # Data models
        ├── research.md    # Technology research
        ├── quickstart.md  # Setup guide
        └── contracts/     # API contracts
```

## API Documentation

The backend provides interactive API documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI spec**: `specs/001-document-compare/contracts/openapi.yaml`

### Main Endpoints

- `GET /api/v1/health` - Health check
- `POST /api/v1/compare` - Compare two documents

## Development

### Code Quality

**Backend:**
```bash
cd backend
poetry run black src tests     # Format code
poetry run ruff check src tests # Lint code
poetry run mypy src            # Type check
```

**Frontend:**
```bash
cd frontend
npm run format      # Format with Prettier
npm run lint        # Lint with ESLint
npm run type-check  # TypeScript check
```

### Constitution Compliance

This project follows a strict constitution (see `.specify/memory/constitution.md`) that enforces:
- Type safety (TypeScript strict mode, Python type hints)
- API design excellence (RESTful, proper error handling, CORS)
- User experience priority (responsive, accessible, clear errors)
- Testing discipline (70%+ coverage for business logic)
- Code quality standards (formatting, linting, no commented code)

## Contributing

1. Read the constitution: `.specify/memory/constitution.md`
2. Check the specification: `specs/001-document-compare/spec.md`
3. Review the technical plan: `specs/001-document-compare/plan.md`
4. Follow the tasks: `specs/001-document-compare/tasks.md`
5. Ensure all quality checks pass before committing

## License

[License information to be added]

## Support

For issues and questions, please check:
1. The quickstart guide: `specs/001-document-compare/quickstart.md`
2. API documentation: http://localhost:8000/docs
3. GitHub issues (after repository is created)
