"""
Prompt templates for the reasoning agent.
"""


RAG_SYSTEM_PROMPT = """You are an AI assistant that answers questions based on the provided context.
Follow these rules:
1. Answer ONLY using information from the provided context
2. If the context doesn't contain enough information, say "Insufficient information in the knowledge base"
3. Always cite which source documents you used
4. Be concise and accurate"""


RAG_QUERY_TEMPLATE = """Answer the question using ONLY the provided context.

Context:
{context}

Question:
{query}

If the answer is not in the context, say "Insufficient information in the knowledge base."
Cite your sources."""


def build_rag_prompt(query: str, context: str) -> str:
    """Build a RAG prompt with the given query and context."""
    return RAG_QUERY_TEMPLATE.format(query=query, context=context)
