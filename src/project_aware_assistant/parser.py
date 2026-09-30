from __future__ import annotations

import hashlib
import re
from pathlib import Path

from .models import SectionRecord

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")


def _clean_heading(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _make_section_id(relative_path: str, heading_hierarchy: list[str]) -> str:
    payload = "|".join([relative_path, *heading_hierarchy])
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:12]


def parse_markdown_sections(path: str | Path) -> list[SectionRecord]:
    file_path = Path(path)
    text = file_path.read_text(encoding="utf-8")
    lines = text.splitlines()

    sections: list[SectionRecord] = []
    heading_stack: list[str] = []
    current_title: str | None = None
    current_lines: list[str] = []
    current_start = 1

    def flush_section(end_line: int) -> None:
        nonlocal current_title, current_lines, heading_stack
        if current_title is None:
            return
        heading_hierarchy = list(heading_stack)
        section_text = "\n".join(current_lines).strip()
        relative_path = file_path.name
        section_id = _make_section_id(relative_path, heading_hierarchy)
        sections.append(
            SectionRecord(
                source_path=file_path,
                heading_hierarchy=heading_hierarchy,
                heading_title=current_title,
                section_text=section_text,
                section_id=section_id,
                start_line=current_start,
                end_line=end_line,
                raw_text=section_text,
            )
        )
        current_title = None
        current_lines = []

    for index, line in enumerate(lines, start=1):
        match = HEADING_RE.match(line)
        if match is not None:
            flush_section(index - 1)
            level = len(match.group(1))
            title = _clean_heading(match.group(2))
            if not title:
                continue
            while len(heading_stack) >= level:
                heading_stack.pop()
            heading_stack.append(title)
            current_title = title
            current_lines = []
            current_start = index
            continue

        if current_title is not None:
            current_lines.append(line.rstrip())

    flush_section(len(lines))

    if not sections and text.strip():
        fallback_title = file_path.stem.replace("-", " ").replace("_", " ").strip() or file_path.name
        section_id = _make_section_id(file_path.name, [fallback_title])
        sections.append(
            SectionRecord(
                source_path=file_path,
                heading_hierarchy=[fallback_title],
                heading_title=fallback_title,
                section_text=text.strip(),
                section_id=section_id,
                start_line=1,
                end_line=len(lines),
                raw_text=text.strip(),
            )
        )

    return sections
