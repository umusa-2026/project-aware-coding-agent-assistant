from __future__ import annotations

import argparse
import json
from pathlib import Path

from .indexer import build_section_index
from .result import format_result
from .retriever import retrieve_sections


def build_payload(query: str, root: str | Path, top_k: int = 3, min_score: float = 2.0) -> dict:
    sections = build_section_index(root)
    results = retrieve_sections(query, sections, top_k=top_k, min_score=min_score)

    if not results:
        return {
            "query": query,
            "status": "no_match",
            "message": "No reliable match found.",
            "results": [],
        }

    payload_results = [
        {
            "rank": result.rank,
            "score": result.score,
            "section_id": result.section_id,
            "source_path": result.source_path,
            "heading_hierarchy": result.heading_hierarchy,
            "title": result.title,
            "excerpt": result.excerpt,
            "matched_terms": result.matched_terms,
        }
        for result in results
    ]

    return {
        "query": query,
        "status": "ok",
        "results": payload_results,
    }


def run_cli(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Project-aware Markdown retrieval baseline")
    parser.add_argument("--root", required=True, help="Directory containing Markdown files")
    parser.add_argument("--query", required=True, help="Natural-language search query")
    parser.add_argument("--top-k", type=int, default=3, help="Number of top results to return")
    parser.add_argument("--min-score", type=float, default=2.0, help="Minimum score threshold")
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    args = parser.parse_args(argv)

    root_path = Path(args.root)
    if not root_path.exists():
        parser.error(f"Root directory does not exist: {root_path}")

    payload = build_payload(args.query, root_path, top_k=args.top_k, min_score=args.min_score)
    output = format_result(payload)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(run_cli())
