# Quickstart Guide: Document Comparison Tool

**Feature**: Document Comparison Tool
**Branch**: `001-document-compare`
**Last Updated**: 2025-10-29

## Overview

This guide will help you set up and run the document comparison application locally. The application consists of two parts:
- **Backend**: Python FastAPI server that performs document comparison
- **Frontend**: React TypeScript application with Tailwind CSS

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.11 or higher**
  - Check version: `python3 --version`
  - Download: https://www.python.org/downloads/

- **Node.js 18 or higher**
  - Check version: `node --version`
  - Download: https://nodejs.org/

- **Poetry** (recommended for Python dependency management)
  - Install: `curl -sSL https://install.python-poetry.org | python3 -`
  - Alternative: Use `pip` and `venv`

- **Git**
  - Check version: `git --version`
  - Download: https://git-scm.com/

## Project Structure

```
document-comparer-fullstack/
├── backend/          # Python FastAPI application
│   ├── src/
│   ├── tests/
│   └── pyproject.toml
├── frontend/         # React TypeScript application
│   ├── src/
│   ├── tests/
│   └── package.json
└── README.md
```

## Backend Setup

### 1. Navigate to Backend Directory

```bash
cd backend
```

### 2. Install Dependencies

**Using Poetry (recommended):**
```bash
poetry install
```

**Using pip:**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Run the Backend Server

**Using Poetry:**
```bash
poetry run uvicorn src.main:app --reload --port 8000
```

**Using pip:**
```bash
# Ensure venv is activated
uvicorn src.main:app --reload --port 8000
```

The backend server will start at: http://localhost:8000

### 4. Verify Backend is Running

Open your browser and navigate to:
- API docs (Swagger UI): http://localhost:8000/docs
- Health check: http://localhost:8000/api/v1/health

You should see:
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

## Frontend Setup

### 1. Navigate to Frontend Directory

```bash
# From the project root
cd frontend
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Configure Backend URL

The frontend is pre-configured to connect to `http://localhost:8000`. If your backend runs on a different port, update `src/services/api.ts`:

```typescript
const API_BASE_URL = 'http://localhost:8000';
```

### 4. Run the Frontend Development Server

```bash
npm run dev
```

The frontend will start at: http://localhost:5173

### 5. Open the Application

Navigate to http://localhost:5173 in your browser. You should see the document comparison interface.

## Running Tests

### Backend Tests

```bash
cd backend

# Using Poetry
poetry run pytest

# Using pip (with venv activated)
pytest

# Run with coverage
poetry run pytest --cov=src --cov-report=term-missing
```

### Frontend Tests

```bash
cd frontend

# Run all tests
npm test

# Run tests in watch mode
npm test -- --watch

# Run tests with coverage
npm test -- --coverage
```

## Using the Application

### Step 1: Upload Documents

1. Open the application in your browser (http://localhost:5173)
2. You have two ways to upload files:
   - **Drag and drop**: Drag files from your desktop onto the upload areas
   - **Click to browse**: Click the upload areas to select files

### Step 2: Compare Documents

1. Upload two text files (e.g., `.txt`, `.md`, `.js`, `.py`)
2. Click the "Compare Documents" button
3. Wait for the comparison to complete (usually < 5 seconds)

### Step 3: View Results

The comparison view shows:
- **Side-by-side layout**: Both documents displayed side by side
- **Color-coded changes**:
  - 🟢 Green: Added lines (present in document 2, not in document 1)
  - 🔴 Red: Deleted lines (present in document 1, not in document 2)
  - 🟡 Yellow: Modified lines (changed between documents)
- **Summary stats**: Total changes, additions, deletions, modifications

### Step 4: Navigate Changes

Use keyboard shortcuts to navigate through differences:
- **Arrow Down (↓)**: Jump to next difference
- **Arrow Up (↑)**: Jump to previous difference

The view automatically scrolls to bring each difference into focus.

### Step 5: Synchronized Scrolling

When scrolling one document panel, the other panel automatically scrolls to maintain alignment. This helps you maintain context while reviewing changes.

## Example Files for Testing

Create two simple test files to try the application:

**version1.txt:**
```
Hello World
This is a test document
It has multiple lines
Some lines will be removed
Some lines will stay the same
The end
```

**version2.txt:**
```
Hello Beautiful World
This is a test document
It has multiple lines
Some lines will stay the same
This is a new line
The end
```

Upload both files and you'll see:
- Line 1 modified: "Hello World" → "Hello Beautiful World"
- Line 4 deleted: "Some lines will be removed"
- Line 5 added: "This is a new line"

## Environment Configuration

### Backend Environment Variables

Create a `.env` file in the `backend` directory:

```bash
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=true

# CORS Configuration
CORS_ORIGINS=["http://localhost:5173"]

# File Upload Limits
MAX_FILE_SIZE_MB=10
MAX_COMPARISON_TIMEOUT_SECONDS=10

# Logging
LOG_LEVEL=INFO
```

### Frontend Environment Variables

Create a `.env` file in the `frontend` directory:

```bash
# API Configuration
VITE_API_BASE_URL=http://localhost:8000

# Feature Flags
VITE_ENABLE_ANALYTICS=false
```

## Troubleshooting

### Backend Issues

**Error: Port 8000 already in use**
```bash
# Find and kill the process using port 8000
lsof -ti:8000 | xargs kill -9

# Or run on a different port
uvicorn src.main:app --reload --port 8001
```

**Error: Module not found**
```bash
# Ensure you're in the backend directory and dependencies are installed
cd backend
poetry install  # or pip install -r requirements.txt
```

**Error: CORS issues**
- Check that frontend URL is in CORS_ORIGINS
- Verify backend is running on expected port
- Check browser console for detailed CORS errors

### Frontend Issues

**Error: Cannot connect to backend**
- Verify backend is running: http://localhost:8000/api/v1/health
- Check `VITE_API_BASE_URL` in frontend `.env` file
- Open browser DevTools Network tab to see failed requests

**Error: npm install fails**
```bash
# Clear npm cache and retry
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

**Error: Vite build fails**
- Check Node.js version: `node --version` (should be 18+)
- Update TypeScript: `npm install -D typescript@latest`

### Common Issues

**Files not uploading**
- Check file size (max 10MB)
- Ensure file is text-based (not binary)
- Check browser console for errors

**Diff not showing**
- Verify backend returned valid response (check Network tab)
- Check for JavaScript errors in browser console
- Try refreshing the page

**Keyboard navigation not working**
- Click on the diff viewer area to focus it
- Ensure there are differences to navigate
- Check browser console for errors

## Development Tips

### Hot Reload

Both backend and frontend support hot reload during development:
- **Backend**: Changes to Python files automatically restart the server
- **Frontend**: Changes to React/TypeScript files automatically refresh the browser

### API Documentation

FastAPI provides interactive API documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

Use these to test API endpoints directly without the frontend.

### Code Formatting

**Backend:**
```bash
cd backend
poetry run black src tests
poetry run ruff check src tests
```

**Frontend:**
```bash
cd frontend
npm run format  # Prettier
npm run lint    # ESLint
```

### Type Checking

**Backend:**
```bash
cd backend
poetry run mypy src
```

**Frontend:**
```bash
cd frontend
npm run type-check  # TypeScript compiler check
```

## Next Steps

- Read the full [specification](./spec.md)
- Review the [technical plan](./plan.md)
- Check the [API contracts](./contracts/openapi.yaml)
- Explore the [data model](./data-model.md)

## Getting Help

If you encounter issues:
1. Check this quickstart guide
2. Review error messages in terminal and browser console
3. Check the [research document](./research.md) for implementation details
4. Open an issue on GitHub (after repository is created)

## Production Deployment

For production deployment:
1. Build frontend: `npm run build` (creates `dist/` folder)
2. Serve frontend static files with nginx or similar
3. Run backend with production ASGI server (gunicorn + uvicorn workers)
4. Configure proper CORS origins (not localhost)
5. Set up SSL/TLS certificates
6. Configure environment variables for production
7. Set up monitoring and logging

See deployment documentation (to be created) for detailed instructions.
