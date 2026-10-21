from __future__ import annotations

import json
from typing import Any


def format_result(payload: dict[str, Any]) -> str:

    if payload["status"] == "no_match":
        return "No reliable match found."
    
    # For text output, create human-readable format
    output_lines = []
    output_lines.append(f"Query: {payload['query']}")
    output_lines.append("")
    
    for i, result in enumerate(payload["results"], 1):
        output_lines.append(f"{i}. {result['title']} ({result['source_path']})")
        output_lines.append(f"   Score: {result['score']}")
        output_lines.append(f"   Excerpt: {result['excerpt']}")
        output_lines.append("")
    
    return "\n".join(output_lines)
