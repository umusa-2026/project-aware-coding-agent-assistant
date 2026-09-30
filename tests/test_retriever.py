from pathlib import Path

from project_aware_assistant.indexer import build_section_index
from project_aware_assistant.retriever import retrieve_sections


def test_retrieve_sections_prefers_exact_topic_matches(tmp_path: Path):
    root = tmp_path / "corpus"
    root.mkdir()
    (root / "project_a.md").write_text(
        "# Overview\n"
        "The system stores debugging notes.\n\n"
        "## Root cause\n"
        "The bug came from a missing environment variable and a broken config path.\n",
        encoding="utf-8",
    )
    (root / "project_b.md").write_text(
        "# Notes\n"
        "This document covers the project config path and environment variable notes.\n",
        encoding="utf-8",
    )

    sections = build_section_index(root)
    results = retrieve_sections("missing environment variable config path", sections, top_k=3)

    assert results[0].source_path.endswith("project_a.md")
    assert results[0].score > results[1].score
    assert "missing" in results[0].excerpt.lower()
