

# ===============================================================================#
# ==================== Retrieve_internal_documents TOOL =========================#
# ===============================================================================#


from langchain_core.tools import tool
from schemas import RetrieveInternalDocsInput
from rag.retriever import search_documents


@tool(args_schema=RetrieveInternalDocsInput)
def Retrieve_internal_documents(query: str) -> str:
    """
    Search the internal documents for relevant information.

    Use this tool when the user asks for factual or
    domain-specific information that should come from
    the uploaded documents.
    """

    try:
        docs = search_documents(query)

        if not docs:
            return "No relevant documents found."

        formatted_docs = []

        for doc in docs:
            source = doc.metadata.get("source", "Unknown Document")
            page = doc.metadata.get("page", "Unknown")

            formatted_docs.append(
                f"[Source: {source} | Page: {page}]\n"
                f"Content: {doc.page_content}"
            )

        return "\n\n---\n\n".join(formatted_docs)

    except Exception:
        return "Error during document retrieval."