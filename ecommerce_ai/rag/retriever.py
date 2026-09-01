
# Chroma -> Semantic Search
# BM25   -> Keyword Search
# EnsembleRetriever -> Hybrid Retrieval

from rag.vectorstore import create_vectorstore

from langchain_classic.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain_core.documents import Document


def search_documents(query: str, k: int = 3):

    # -----------------------------
    # Create / Load Chroma VectorStore
    # -----------------------------
    vectorstore = create_vectorstore()

    # -----------------------------
    # Read data from Chroma
    # -----------------------------
    data = vectorstore.get()

    print(data.keys())
    #print(data)

    # -----------------------------
    # Semantic Retrieval - Chroma
    # -----------------------------
    semantic_retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": k
        },
    )

    # -----------------------------
    # Keyword Retrieval - BM25
    # -----------------------------
    documents = data["documents"]
    metadatas = data.get("metadatas")

    # Convert Chroma documents into LangChain Document objects
    # so BM25 keeps the original metadata.
    if metadatas:
        keyword_documents = [
            Document(
                page_content=document,
                metadata=metadata or {}
            )
            for document, metadata in zip(documents, metadatas)
        ]
    else:
        keyword_documents = [
            Document(
                page_content=document
            )
            for document in documents
        ]

    keyword_retriever = BM25Retriever.from_documents(
        keyword_documents
    )

    keyword_retriever.k = k

    # -----------------------------
    # Hybrid Retrieval
    # -----------------------------
    retriever = EnsembleRetriever(
        retrievers=[
            semantic_retriever,
            keyword_retriever
        ],
        weights=[
            0.5,
            0.5
        ],
    )

    # -----------------------------
    # Retrieve Documents
    # -----------------------------
    documents = retriever.invoke(query)

    # -----------------------------
    # Return Top K Documents
    # -----------------------------
    return documents[:k]

