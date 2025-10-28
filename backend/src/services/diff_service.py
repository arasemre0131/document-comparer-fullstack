"""
Document comparison service using Python's difflib.
"""

import difflib
from typing import List, Tuple

from ..api.models import ChangeType, DiffChange


class DiffService:
    """Service for comparing two text documents."""

    @staticmethod
    def compare_documents(content1: str, content2: str) -> List[DiffChange]:
        """
        Compare two documents and return list of changes.

        Args:
            content1: Content of the first document
            content2: Content of the second document

        Returns:
            List of DiffChange objects representing all differences
        """
        lines1 = content1.splitlines()
        lines2 = content2.splitlines()

        # Use SequenceMatcher for detailed comparison
        matcher = difflib.SequenceMatcher(None, lines1, lines2)
        changes: List[DiffChange] = []

        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == "equal":
                # No change, skip
                continue
            elif tag == "insert":
                # Lines added in document 2
                for j in range(j1, j2):
                    changes.append(
                        DiffChange(
                            change_type=ChangeType.ADD,
                            line_number_old=None,
                            line_number_new=j + 1,
                            old_content=None,
                            new_content=lines2[j] if j < len(lines2) else "",
                            is_modified=False,
                        )
                    )
            elif tag == "delete":
                # Lines removed from document 1
                for i in range(i1, i2):
                    changes.append(
                        DiffChange(
                            change_type=ChangeType.DELETE,
                            line_number_old=i + 1,
                            line_number_new=None,
                            old_content=lines1[i] if i < len(lines1) else "",
                            new_content=None,
                            is_modified=False,
                        )
                    )
            elif tag == "replace":
                # Lines modified between documents
                # Handle as modifications when line counts match, otherwise as delete+add
                if (i2 - i1) == (j2 - j1):
                    # Same number of lines, treat as modifications
                    for idx in range(i2 - i1):
                        i = i1 + idx
                        j = j1 + idx
                        changes.append(
                            DiffChange(
                                change_type=ChangeType.MODIFY,
                                line_number_old=i + 1,
                                line_number_new=j + 1,
                                old_content=lines1[i] if i < len(lines1) else "",
                                new_content=lines2[j] if j < len(lines2) else "",
                                is_modified=True,
                            )
                        )
                else:
                    # Different number of lines, treat as delete + add
                    for i in range(i1, i2):
                        changes.append(
                            DiffChange(
                                change_type=ChangeType.DELETE,
                                line_number_old=i + 1,
                                line_number_new=None,
                                old_content=lines1[i] if i < len(lines1) else "",
                                new_content=None,
                                is_modified=False,
                            )
                        )
                    for j in range(j1, j2):
                        changes.append(
                            DiffChange(
                                change_type=ChangeType.ADD,
                                line_number_old=None,
                                line_number_new=j + 1,
                                old_content=None,
                                new_content=lines2[j] if j < len(lines2) else "",
                                is_modified=False,
                            )
                        )

        return changes

    @staticmethod
    def get_change_statistics(changes: List[DiffChange]) -> Tuple[int, int, int]:
        """
        Calculate statistics from list of changes.

        Args:
            changes: List of DiffChange objects

        Returns:
            Tuple of (additions, deletions, modifications)
        """
        additions = sum(1 for c in changes if c.change_type == ChangeType.ADD)
        deletions = sum(1 for c in changes if c.change_type == ChangeType.DELETE)
        modifications = sum(1 for c in changes if c.change_type == ChangeType.MODIFY)

        return additions, deletions, modifications
