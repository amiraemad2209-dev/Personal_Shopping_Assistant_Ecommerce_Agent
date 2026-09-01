

from langchain_core.prompts import ChatPromptTemplate


RAG_Prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are a document question-answering assistant.

Answer the user's question using ONLY the provided context.

If the answer cannot be found in the context, return:
found = false
and clearly state that no relevant information was found.

Context:
{context}
"""
    ),
    (
        "human",
        "{question}"
    ),
])

