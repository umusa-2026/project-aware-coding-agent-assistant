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
