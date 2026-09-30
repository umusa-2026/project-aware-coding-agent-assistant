from __future__ import annotations

from .models import SectionRecord
from .ranking import rank_sections


def retrieve_sections(query: str, sections: list[SectionRecord], top_k: int = 3, min_score: float = 2.0):
    if not query or not query.strip():
        return []
    return rank_sections(query, sections, top_k=top_k, min_score=min_score)
