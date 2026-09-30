from __future__ import annotations

import json
from typing import Any


def format_result(payload: dict[str, Any]) -> str:
    return json.dumps(payload, indent=2, sort_keys=True)
