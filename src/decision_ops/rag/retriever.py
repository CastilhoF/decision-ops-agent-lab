from __future__ import annotations

import re
from pathlib import Path

from decision_ops.domain.models import KnowledgeChunk


class LexicalRetriever:
    """Small offline retriever used to make RAG mechanics easy to inspect.

    Production systems commonly replace this lexical ranker with embeddings plus
    vector search, often retaining lexical search as a complementary signal.
    """

    def __init__(self, knowledge_directory: Path):
        self.knowledge_directory = knowledge_directory

    def search(self, query: str, limit: int = 3) -> list[KnowledgeChunk]:
        query_terms = self._terms(query)
        matches: list[KnowledgeChunk] = []
        for path in sorted(self.knowledge_directory.glob("*.md")):
            for chunk in self._chunks(path):
                overlap = len(query_terms & self._terms(chunk))
                if overlap:
                    matches.append(
                        KnowledgeChunk(
                            source=str(path.relative_to(self.knowledge_directory.parent.parent)),
                            content=chunk,
                            score=overlap / max(len(query_terms), 1),
                        )
                    )
        return sorted(matches, key=lambda item: (-item.score, item.source))[:limit]

    @staticmethod
    def _terms(value: str) -> set[str]:
        return {token.lower() for token in re.findall(r"[a-zA-Z]{3,}", value)}

    @staticmethod
    def _chunks(path: Path) -> list[str]:
        text = path.read_text(encoding="utf-8").strip()
        chunks = (chunk.strip() for chunk in text.split("\n\n"))
        return [chunk for chunk in chunks if chunk and not chunk.startswith("#")]
