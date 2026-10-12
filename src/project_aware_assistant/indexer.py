from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from .models import IndexBundle, SectionRecord
from .parser import parse_markdown_sections


def discover_markdown_files(root: str | Path) -> list[Path]:
    corpus_root = Path(root)
    results = sorted(path for path in corpus_root.rglob("*.md") if path.is_file())
    return results


def build_section_index(root: str | Path) -> list[SectionRecord]:
    corpus_root = Path(root)
    sections: list[SectionRecord] = []
    for file_path in discover_markdown_files(corpus_root):
        # Pass the corpus root to parse_markdown_sections
        sections.extend(parse_markdown_sections(file_path, corpus_root))
    return sections


def build_index_bundle(root: str | Path) -> IndexBundle:
    corpus_root = Path(root)
    files = discover_markdown_files(corpus_root)
    sections = build_section_index(corpus_root)
    return IndexBundle(
        corpus_root=str(corpus_root),
        files_scanned=len(files),
        sections_indexed=len(sections),
        generated_at=datetime.now(timezone.utc).isoformat(),
    )
