from pathlib import Path

from project_aware_assistant.parser import parse_markdown_sections


def test_parse_markdown_sections_creates_hierarchy(tmp_path: Path):
    path = tmp_path / "sample.md"
    path.write_text(
        "# Overview\n"
        "Intro text.\n\n"
        "## Build\n"
        "Build the project.\n\n"
        "### Local setup\n"
        "Use Python 3.11.\n",
        encoding="utf-8",
    )

    sections = parse_markdown_sections(path)

    assert len(sections) == 3
    assert sections[0].heading_hierarchy == ["Overview"]
    assert sections[1].heading_hierarchy == ["Overview", "Build"]
    assert sections[2].heading_hierarchy == ["Overview", "Build", "Local setup"]
    assert sections[0].section_id
    assert "python" in sections[2].section_text.lower()
