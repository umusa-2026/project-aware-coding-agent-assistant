from pathlib import Path

from project_aware_assistant.indexer import build_section_index, discover_markdown_files


def test_discover_markdown_files_and_index(tmp_path: Path):
    root = tmp_path / "corpus"
    root.mkdir()
    nested = root / "nested"
    nested.mkdir()
    (root / "a.md").write_text("# Alpha\nAlpha text.\n", encoding="utf-8")
    (nested / "b.md").write_text("# Beta\nBeta text.\n", encoding="utf-8")

    files = discover_markdown_files(root)
    assert len(files) == 2

    sections = build_section_index(root)
    assert len(sections) == 2
    assert {section.source_path.name for section in sections} == {"a.md", "b.md"}
    assert all(section.section_id for section in sections)
