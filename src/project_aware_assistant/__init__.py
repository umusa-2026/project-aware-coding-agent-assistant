"""Project-aware coding assistant retrieval MVP."""

from .indexer import build_section_index, discover_markdown_files
from .models import IndexBundle, QueryResult, SectionRecord
from .parser import parse_markdown_sections
from .retriever import retrieve_sections

__all__ = [
    "IndexBundle",
    "QueryResult",
    "SectionRecord",
    "build_section_index",
    "discover_markdown_files",
    "parse_markdown_sections",
    "retrieve_sections",
]
