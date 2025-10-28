"""
File validation utilities.
"""

from typing import Tuple

# Maximum file size: 10MB
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024

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
    Validate that file is a text file based on extension and content.

    Args:
        filename: Name of the file
        content: File content as bytes

    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check extension
    import os

    _, ext = os.path.splitext(filename.lower())

    if ext and ext not in TEXT_EXTENSIONS:
        return (
            False,
            f"File type '{ext}' not supported. Please upload a text-based file.",
        )

    # Try to decode as text
    try:
        content.decode("utf-8")
    except UnicodeDecodeError:
        try:
            content.decode("latin-1")
        except UnicodeDecodeError:
            return False, "File must be a text document, binary files not supported"

    return True, ""


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
