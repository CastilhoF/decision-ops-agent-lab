# RAG: retrieval before generation

RAG means Retrieval-Augmented Generation. The system first retrieves relevant external evidence, then supplies that evidence to an LLM while it generates an answer.

In this project:

1. Markdown files in `data/knowledge/` are the knowledge base.
2. `LexicalRetriever` splits them into paragraphs.
3. A query is tokenized and ranked by term overlap.
4. The API returns chunks with their source path and score.
5. The LLM agent can call the same retrieval capability as a tool.

The lexical ranker is intentionally simple so the whole loop can be inspected. A production evolution would add ingestion metadata, chunk sizes and overlap, embeddings, vector search, hybrid ranking, filtering, and retrieval evaluation. Those are retrieval concerns; the answer model remains a separate concern.

The practical rule: always return source metadata to the caller. If you cannot show why a chunk was retrieved, it is hard to debug a hallucinated answer.
