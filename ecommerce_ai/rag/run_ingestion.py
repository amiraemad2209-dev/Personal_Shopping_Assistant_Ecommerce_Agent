

from rag.loaders import load_document
from rag.chunking import semantic_chunk_documents
from rag.indexing import add_documents


def ingest_document(file_path: str):

    # 1. Load document
    documents = load_document(file_path)

    print(
        f"Loaded {len(documents)} documents."
    )

    # 2. Semantic chunking
    chunks = semantic_chunk_documents(documents)

    print(
        f"Created {len(chunks)} chunks."
    )

    # 3. Index into Chroma
    result = add_documents(chunks)

    print(
        f"Indexing result: {result}"
    )

    return result