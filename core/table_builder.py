"""Markdown Table Builder — Programmatic markdown table generation.

Provides a fluent API for building aligned markdown tables
with column alignment, sorting, and filtering.
"""

from collections.abc import Callable
from typing import Any


class TableBuilder:
    """Fluent API for building markdown tables."""

    def __init__(self):
        self._columns: list[tuple[str, str]] = []  # (name, alignment)
        self._rows: list[list[str]] = []

    def add_column(self, name: str, align: str = "left") -> "TableBuilder":
        """Add a column. align: 'left', 'center', 'right'."""
        self._columns.append((name, align))
        return self

    def add_row(self, *values: Any) -> "TableBuilder":
        """Add a row of values."""
        self._rows.append([str(v) for v in values])
        return self

    def add_rows(self, rows: list[list[Any]]) -> "TableBuilder":
        """Add multiple rows."""
        for row in rows:
            self.add_row(*row)
        return self

    def sort_by(self, column_index: int, reverse: bool = False) -> "TableBuilder":
        """Sort rows by a column index."""
        self._rows.sort(
            key=lambda r: r[column_index] if column_index < len(r) else "",
            reverse=reverse,
        )
        return self

    def filter_rows(self, predicate: Callable[[list[str]], bool]) -> "TableBuilder":
        """Filter rows using a predicate."""
        self._rows = [r for r in self._rows if predicate(r)]
        return self

    def build(self) -> str:
        """Build the markdown table string."""
        if not self._columns:
            return ""

        # Header
        header = "| " + " | ".join(name for name, _ in self._columns) + " |"

        # Separator with alignment
        sep_parts = []
        for _, align in self._columns:
            if align == "center":
                sep_parts.append(":---:")
            elif align == "right":
                sep_parts.append("---:")
            else:
                sep_parts.append("---")
        separator = "| " + " | ".join(sep_parts) + " |"

        # Rows
        lines = [header, separator]
        for row in self._rows:
            # Pad row to match column count
            padded = row + [""] * (len(self._columns) - len(row))
            lines.append("| " + " | ".join(padded[: len(self._columns)]) + " |")

        return "\n".join(lines)

    @property
    def row_count(self) -> int:
        return len(self._rows)

    @property
    def column_count(self) -> int:
        return len(self._columns)

    def to_dict(self) -> dict[str, Any]:
        return {
            "columns": [{"name": n, "align": a} for n, a in self._columns],
            "rows": self._rows,
            "row_count": self.row_count,
        }
