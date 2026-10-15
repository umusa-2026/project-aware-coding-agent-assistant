import json

from project_aware_assistant.cli import run_cli


def test_cli_reports_no_match_for_low_signal(tmp_path, capsys):
    root = tmp_path / "corpus"
    root.mkdir()
    (root / "notes.md").write_text("# Team updates\nWe met yesterday and discussed planning.\n", encoding="utf-8")

    exit_code = run_cli([
        "--root",
        str(root),
        "--query",
        "impossible environment variable debugging failure",
        "--json",
    ])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)

    assert exit_code == 0
    assert payload["status"] == "no_match"
    assert payload["results"] == []


def test_successful_json_query_returns_expected_fields(tmp_path, capsys):
    """Test that successful JSON query returns status 'ok', ranked results, and expected result fields"""
    root = tmp_path / "corpus"
    root.mkdir()
    (root / "notes.md").write_text("# Team updates\nWe met yesterday and discussed planning.\n", encoding="utf-8")

    exit_code = run_cli([
        "--root",
        str(root),
        "--query",
        "planning",
        "--json",
    ])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)

    assert exit_code == 0
    assert payload["status"] == "ok"
    assert len(payload["results"]) > 0
    assert "rank" in payload["results"][0]
    assert "score" in payload["results"][0]
    assert "section_id" in payload["results"][0]
    assert "source_path" in payload["results"][0]
    assert "heading_hierarchy" in payload["results"][0]
    assert "title" in payload["results"][0]
    assert "excerpt" in payload["results"][0]
    assert "matched_terms" in payload["results"][0]


def test_text_output_contains_matched_source_title(tmp_path, capsys):
    """Test that text output for successful query contains the matched source/title"""
    root = tmp_path / "corpus"
    root.mkdir()
    (root / "notes.md").write_text("# Team updates\nWe met yesterday and discussed planning.\n", encoding="utf-8")

    exit_code = run_cli([
        "--root",
        str(root),
        "--query",
        "planning",
    ])

    captured = capsys.readouterr()
    output = captured.out

    assert exit_code == 0
    assert "Team updates" in output  # Should contain the title
    assert "notes.md" in output     # Should contain the source file


def test_json_and_text_modes_use_same_no_match_decision(tmp_path, capsys):
    """Test that JSON and text modes use the same no-match decision"""
    root = tmp_path / "corpus"
    root.mkdir()
    (root / "notes.md").write_text("# Team updates\nWe met yesterday and discussed planning.\n", encoding="utf-8")

    # Test JSON mode
    exit_code_json = run_cli([
        "--root",
        str(root),
        "--query",
        "impossible environment variable debugging failure",
        "--json",
    ])
    
    captured_json = capsys.readouterr()
    payload_json = json.loads(captured_json.out)

    # Test text mode
    exit_code_text = run_cli([
        "--root",
        str(root),
        "--query",
        "impossible environment variable debugging failure",
    ])
    
    captured_text = capsys.readouterr()
    output_text = captured_text.out

    assert exit_code_json == 0
    assert exit_code_text == 0
    assert payload_json["status"] == "no_match"
    # Both should report no match
    assert "No reliable match found" in output_text or "no_match" in output_text.lower()
