"""
Prompt templates for the reasoning agent.
"""


RAG_SYSTEM_PROMPT = """You are an AI assistant that answers questions based on the provided context.
Follow these rules:
1. Answer ONLY using information from the provided context
2. If the context doesn't contain enough information, say "Insufficient information in the knowledge base"
3. Always cite which source documents you used
4. Be concise and accurate"""


RAG_QUERY_TEMPLATE = """You are a helpful assistant. Read the following context carefully and answer the user's question.

CONTEXT:
{context}

USER QUESTION: {query}

INSTRUCTIONS:
- Answer the question based on the context above
- Be specific and extract relevant details from the context
- If the context contains information related to the question, provide that information
- Only say "Insufficient information" if the context truly has NO relevant information
- Cite the source document(s) used

ANSWER:"""


def build_rag_prompt(query: str, context: str) -> str:
    """Build a RAG prompt with the given query and context."""
    return RAG_QUERY_TEMPLATE.format(query=query, context=context)
