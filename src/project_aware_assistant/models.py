from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class SectionRecord:
    source_path: Path
    heading_hierarchy: list[str]
    heading_title: str
    section_text: str
    section_id: str
    start_line: int = 1
    end_line: int = 1
    raw_text: str = ""


@dataclass
class QueryResult:
    rank: int
    score: float
    section_id: str
    source_path: str
    heading_hierarchy: list[str]
    title: str
    excerpt: str
    matched_terms: list[str] = field(default_factory=list)


@dataclass
class IndexBundle:
    corpus_root: str
    files_scanned: int
    sections_indexed: int
    generated_at: str
