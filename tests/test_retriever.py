from pathlib import Path

from decision_ops.rag.retriever import LexicalRetriever


def test_retrieves_approval_policy_for_approval_question() -> None:
    retriever = LexicalRetriever(Path("data/knowledge"))

    results = retriever.search("When is human approval required?")

    assert results
    assert results[0].source == "data/knowledge/approval-policy.md"
    assert "human planner review" in results[0].content


def test_returns_no_evidence_for_unrelated_question() -> None:
    retriever = LexicalRetriever(Path("data/knowledge"))

    assert retriever.search("How do I bake a sourdough loaf?") == []
