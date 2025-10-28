"""
Pydantic models for API request and response validation.
"""

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


class ChangeType(str, Enum):
    """Type of change between documents."""

    ADD = "add"
    DELETE = "delete"
    MODIFY = "modify"


class DiffChange(BaseModel):
    """Represents a single change between two documents."""

    change_type: ChangeType
    line_number_old: Optional[int] = None
    line_number_new: Optional[int] = None
    old_content: Optional[str] = None
    new_content: Optional[str] = None
    is_modified: bool = False

    @field_validator("old_content")
    @classmethod
    def validate_old_content(cls, v: Optional[str], info) -> Optional[str]:
        """Validate old_content based on change_type."""
        change_type = info.data.get("change_type")
        if change_type == ChangeType.ADD and v is not None:
            raise ValueError("old_content must be null for ADD changes")
        if change_type == ChangeType.DELETE and v is None:
            raise ValueError("old_content must be present for DELETE changes")
        return v

    @field_validator("new_content")
    @classmethod
    def validate_new_content(cls, v: Optional[str], info) -> Optional[str]:
        """Validate new_content based on change_type."""
        change_type = info.data.get("change_type")
        if change_type == ChangeType.DELETE and v is not None:
            raise ValueError("new_content must be null for DELETE changes")
        if change_type == ChangeType.ADD and v is None:
            raise ValueError("new_content must be present for ADD changes")
        return v


class ComparisonResult(BaseModel):
    """Result of comparing two documents."""

    document1_name: str
    document2_name: str
    total_changes: int = Field(ge=0)
    additions: int = Field(ge=0)
    deletions: int = Field(ge=0)
    modifications: int = Field(ge=0)
    changes: List[DiffChange]
    compared_at: datetime = Field(default_factory=lambda: datetime.utcnow())
    is_identical: bool

    @field_validator("total_changes")
    @classmethod
    def validate_total_changes(cls, v: int, info) -> int:
        """Validate total_changes equals sum of additions, deletions, and modifications."""
        additions = info.data.get("additions", 0)
        deletions = info.data.get("deletions", 0)
        modifications = info.data.get("modifications", 0)
        expected = additions + deletions + modifications
        if v != expected:
            raise ValueError(
                f"total_changes ({v}) must equal additions + deletions + modifications ({expected})"
            )
        return v

    @field_validator("is_identical")
    @classmethod
    def validate_is_identical(cls, v: bool, info) -> bool:
        """Validate is_identical is True when total_changes is 0."""
        total_changes = info.data.get("total_changes", -1)
        if total_changes == 0 and not v:
            raise ValueError("is_identical must be True when total_changes is 0")
        if total_changes > 0 and v:
            raise ValueError("is_identical must be False when total_changes > 0")
        return v


class ErrorResponse(BaseModel):
    """Error response model."""

    detail: str
    error_code: str


class HealthResponse(BaseModel):
    """Health check response model."""

    status: str
    version: str
