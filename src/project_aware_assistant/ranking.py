from __future__ import annotations

import math
import re
from collections import Counter

from .models import QueryResult, SectionRecord


TOKEN_RE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)?")

STOP_WORDS = frozenset({
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "that",
    "the",
    "to",
    "was",
    "were",
    "with",
})

MIN_QUERY_COVERAGE = 0.6

def _tokenize(text: str) -> list[str]:
    return TOKEN_RE.findall(text.lower())

def _meaningful_tokens(text: str) -> list[str]:
    return [
        token
        for token in _tokenize(text)
        if token not in STOP_WORDS
    ]


def _contains_token_phrase(
    tokens: list[str],
    phrase_tokens: list[str],
) -> bool:
    phrase_length = len(phrase_tokens)
    if phrase_length == 0 or phrase_length > len(tokens):
        return False

    return any(
        tokens[start:start + phrase_length] == phrase_tokens
        for start in range(len(tokens) - phrase_length + 1)
    )

def _score_section(
    query: str,
    section: SectionRecord,
) -> tuple[float, list[str]]:
    query_tokens = _meaningful_tokens(query)
    if not query_tokens:
        return 0.0, []

    section_text = "\n".join([
        " ".join(section.heading_hierarchy),
        section.section_text,
    ])
    section_tokens = _meaningful_tokens(section_text)
    section_token_set = set(section_tokens)

    unique_query_terms = set(query_tokens)
    overlap = unique_query_terms & section_token_set
    query_coverage = len(overlap) / len(unique_query_terms)
    if query_coverage < MIN_QUERY_COVERAGE:
        return 0.0, []

    section_counter = Counter(section_tokens)

    title_tokens = _meaningful_tokens(
        " ".join(section.heading_hierarchy)
    )
    title_counter = Counter(title_tokens)

    score = 0.0
    matched_terms: list[str] = []

    for token in query_tokens:
        if token in section_counter:
            score += section_counter[token] * 2.0
            matched_terms.append(token)

        if token in title_counter:
            score += title_counter[token] * 5.0
            if token not in matched_terms:
                matched_terms.append(token)

    score += len(overlap) * 3.0

    if _contains_token_phrase(section_tokens, query_tokens):
        score += 10.0

    if unique_query_terms <= section_token_set:
        score += 2.0

    return score, matched_terms

def rank_sections(query: str, sections: list[SectionRecord], top_k: int = 3, min_score: float = 2.0) -> list[QueryResult]:
    ranked: list[tuple[float, str, SectionRecord, list[str]]] = []
    for section in sections:
        score, matched_terms = _score_section(query, section)
        if score < min_score:
            continue
        ranked.append((score, section.section_id, section, matched_terms))

    ranked.sort(key=lambda item: (-item[0], item[1]))

    results: list[QueryResult] = []
    for index, (_, section_id, section, matched_terms) in enumerate(ranked[:top_k], start=1):
        snippet = section.section_text.strip().replace("\n", " ")
        snippet = re.sub(r"\s+", " ", snippet)[:180]
        results.append(
            QueryResult(
                rank=index,
                score=round(float(_score_section(query, section)[0]), 4),
                section_id=section_id,
                source_path=str(section.source_path),
                heading_hierarchy=list(section.heading_hierarchy),
                title=section.heading_title,
                excerpt=snippet,
                matched_terms=matched_terms,
            )
        )

    return results
