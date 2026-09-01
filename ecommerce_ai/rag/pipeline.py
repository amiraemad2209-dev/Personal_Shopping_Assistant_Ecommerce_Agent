

from rag.retriever import search_documents
from schemas import RAGResponse
from rag.RAG_Prompt import RAG_Prompt
from models import DocumentSearch_llm 


def rag_pipeline(query: str) -> RAGResponse:

    documents = search_documents(
        query=query,
        k=5,
    )

    if not documents:

        return RAGResponse(
            answer=(
                "No relevant information was found "
                "in the indexed documents."
            ),
            sources=[],
            found=False,
        )

    context_parts = []

    sources = []

    for document in documents:

        source = document.metadata.get(
            "source",
            "unknown",
        )

        content = document.page_content

        context_parts.append(
            f"Source: {source}\n"
            f"Content:\n{content}"
        )

        sources.append(
            {
                "source": source,
                "content": content,
            }
        )

    context = "\n\n".join(context_parts)

    chain = RAG_Prompt | DocumentSearch_llm

    response = chain.invoke(
        {
            "question": query,
            "context": context,
        }
    )

    # Ensure sources come from retrieval
    response.sources = sources

    return response