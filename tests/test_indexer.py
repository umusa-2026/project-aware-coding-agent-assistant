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

def test_same_filename_and_heading_in_different_directories_have_unique_ids(
    tmp_path: Path,
):
    root = tmp_path / "corpus"
    first_directory = root / "a"
    second_directory = root / "b"
    first_directory.mkdir(parents=True)
    second_directory.mkdir(parents=True)

    (first_directory / "note.md").write_text(
        "# Same\nAlpha text.\n",
        encoding="utf-8",
    )
    (second_directory / "note.md").write_text(
        "# Same\nBeta text.\n",
        encoding="utf-8",
    )

    sections = build_section_index(root)

    assert len(sections) == 2
    assert sections[0].section_id != sections[1].section_id


def test_section_ids_do_not_depend_on_absolute_corpus_path(tmp_path: Path):
    first_root = tmp_path / "first" / "corpus"
    second_root = tmp_path / "second" / "corpus"

    for root in (first_root, second_root):
        document_directory = root / "nested"
        document_directory.mkdir(parents=True)
        (document_directory / "note.md").write_text(
            "# Overview\nStable content.\n",
            encoding="utf-8",
        )

    first_sections = build_section_index(first_root)
    second_sections = build_section_index(second_root)

    assert len(first_sections) == 1
    assert len(second_sections) == 1
    assert first_sections[0].section_id == second_sections[0].section_id
