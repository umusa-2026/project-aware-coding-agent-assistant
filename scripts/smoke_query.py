from __future__ import annotations

from project_aware_assistant.cli import run_cli


if __name__ == "__main__":
    raise SystemExit(
        run_cli([
            "--root",
            "data/corpora/synthetic",
            "--query",
            "missing environment variable config path",
            "--top-k",
            "3",
        ])
    )
