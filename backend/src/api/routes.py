"""
API routes for document comparison.
"""

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse

from .models import ComparisonResult, ErrorResponse, HealthResponse
from ..services.diff_service import DiffService
from ..utils.validators import (
    decode_file_content,
    extract_pdf_text,
    validate_file_size,
    validate_file_type,
)

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint."""
    return HealthResponse(status="healthy", version="1.0.0")


@router.post("/compare", response_model=ComparisonResult, responses={
    400: {"model": ErrorResponse},
    500: {"model": ErrorResponse},
})
async def compare_documents(
    file1: UploadFile = File(..., description="First document to compare"),
    file2: UploadFile = File(..., description="Second document to compare"),
) -> ComparisonResult:
    """
    Compare two text documents and return highlighted differences.

    Args:
        file1: First document file
        file2: Second document file

    Returns:
        ComparisonResult with all differences between documents

    Raises:
        HTTPException: If files are invalid or comparison fails
    """
    try:
        # Read file contents
        content1_bytes = await file1.read()
        content2_bytes = await file2.read()

        # Validate file sizes
        is_valid, error_msg = validate_file_size(content1_bytes)
        if not is_valid:
            raise HTTPException(
                status_code=400,
                detail=error_msg,
            )

        is_valid, error_msg = validate_file_size(content2_bytes)
        if not is_valid:
            raise HTTPException(
                status_code=400,
                detail=error_msg,
            )

        # Validate file types
        is_valid, error_msg = validate_file_type(file1.filename or "", content1_bytes)
        if not is_valid:
            raise HTTPException(
                status_code=400,
                detail=error_msg,
            )

        is_valid, error_msg = validate_file_type(file2.filename or "", content2_bytes)
        if not is_valid:
            raise HTTPException(
                status_code=400,
                detail=error_msg,
            )

        # Decode file contents (handle PDF and text files)
        try:
            import os

            # Check if files are PDFs
            _, ext1 = os.path.splitext((file1.filename or "").lower())
            _, ext2 = os.path.splitext((file2.filename or "").lower())

            if ext1 == ".pdf":
                content1 = extract_pdf_text(content1_bytes)
            else:
                content1, _ = decode_file_content(content1_bytes)

            if ext2 == ".pdf":
                content2 = extract_pdf_text(content2_bytes)
            else:
                content2, _ = decode_file_content(content2_bytes)

        except UnicodeDecodeError as e:
            raise HTTPException(
                status_code=400,
                detail=f"Unable to decode file: {str(e)}",
            )
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Error processing file: {str(e)}",
            )

        # Perform comparison
        diff_service = DiffService()
        changes = diff_service.compare_documents(content1, content2)
        additions, deletions, modifications = diff_service.get_change_statistics(changes)

        # Build response
        result = ComparisonResult(
            document1_name=file1.filename or "document1",
            document2_name=file2.filename or "document2",
            total_changes=len(changes),
            additions=additions,
            deletions=deletions,
            modifications=modifications,
            changes=changes,
            is_identical=len(changes) == 0,
        )

        return result

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Catch any other exceptions
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while comparing documents: {str(e)}",
        )
