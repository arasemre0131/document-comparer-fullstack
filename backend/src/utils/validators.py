"""
File validation utilities.
"""

import os
from typing import Tuple

try:
    from PyPDF2 import PdfReader
except ImportError:
    PdfReader = None  # type: ignore

# Maximum file size: 10MB
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024

# Maximum pages for PDF files
MAX_PDF_PAGES = 10

# Supported text file extensions
TEXT_EXTENSIONS = {
    ".txt",
    ".md",
    ".py",
    ".js",
    ".ts",
    ".jsx",
    ".tsx",
    ".json",
    ".yaml",
    ".yml",
    ".xml",
    ".html",
    ".css",
    ".scss",
    ".java",
    ".c",
    ".cpp",
    ".h",
    ".hpp",
    ".rs",
    ".go",
    ".rb",
    ".php",
    ".sh",
    ".bash",
    ".sql",
    ".r",
    ".m",
    ".swift",
    ".kt",
    ".scala",
    ".log",
    ".csv",
    ".properties",
    ".ini",
    ".conf",
    ".config",
    ".pdf",  # PDF support added
}


def validate_file_size(content: bytes) -> Tuple[bool, str]:
    """
    Validate that file size is within acceptable limits.

    Args:
        content: File content as bytes

    Returns:
        Tuple of (is_valid, error_message)
    """
    if len(content) > MAX_FILE_SIZE_BYTES:
        return False, f"File size exceeds maximum limit of {MAX_FILE_SIZE_BYTES // (1024 * 1024)}MB"
    return True, ""


def validate_file_type(filename: str, content: bytes) -> Tuple[bool, str]:
    """
    Validate that file is a text file or PDF based on extension and content.

    Args:
        filename: Name of the file
        content: File content as bytes

    Returns:
        Tuple of (is_valid, error_message)
    """
    _, ext = os.path.splitext(filename.lower())

    if ext and ext not in TEXT_EXTENSIONS:
        return (
            False,
            f"File type '{ext}' not supported. Please upload a text-based file or PDF.",
        )

    # PDF files are validated separately
    if ext == ".pdf":
        return validate_pdf(content)

    # Try to decode as text
    try:
        content.decode("utf-8")
    except UnicodeDecodeError:
        try:
            content.decode("latin-1")
        except UnicodeDecodeError:
            return False, "File must be a text document or PDF"

    return True, ""


def validate_pdf(content: bytes) -> Tuple[bool, str]:
    """
    Validate PDF file and check page count.

    Args:
        content: PDF file content as bytes

    Returns:
        Tuple of (is_valid, error_message)
    """
    if PdfReader is None:
        return False, "PDF support not available (PyPDF2 not installed)"

    try:
        import io
        pdf_reader = PdfReader(io.BytesIO(content))
        page_count = len(pdf_reader.pages)

        if page_count > MAX_PDF_PAGES:
            return False, f"PDF has {page_count} pages, maximum allowed is {MAX_PDF_PAGES}"

        return True, ""
    except Exception as e:
        return False, f"Invalid PDF file: {str(e)}"


def extract_pdf_text(content: bytes) -> str:
    """
    Extract text from PDF file.

    Args:
        content: PDF file content as bytes

    Returns:
        Extracted text content

    Raises:
        Exception: If PDF cannot be read or parsed
    """
    if PdfReader is None:
        raise Exception("PDF support not available (PyPDF2 not installed)")

    try:
        import io
        pdf_reader = PdfReader(io.BytesIO(content))

        text_parts = []
        for page_num, page in enumerate(pdf_reader.pages, 1):
            page_text = page.extract_text()
            text_parts.append(f"--- Page {page_num} ---\n{page_text}")

        return "\n\n".join(text_parts)
    except Exception as e:
        raise Exception(f"Failed to extract text from PDF: {str(e)}")


def decode_file_content(content: bytes) -> Tuple[str, str]:
    """
    Decode file content to string, trying multiple encodings.

    Args:
        content: File content as bytes

    Returns:
        Tuple of (decoded_content, encoding_used)

    Raises:
        UnicodeDecodeError: If file cannot be decoded with any supported encoding
    """
    encodings = ["utf-8", "latin-1", "ascii", "iso-8859-1"]

    for encoding in encodings:
        try:
            decoded = content.decode(encoding)
            return decoded, encoding
        except UnicodeDecodeError:
            continue

    raise UnicodeDecodeError(
        "unknown", content, 0, len(content), "Unable to decode file with any supported encoding"
    )
