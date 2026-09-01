
#اتفقنا إن create_vectorstore() بيرجع Chroma VectorStore،
#والأفضل نحافظ على الـmetadata أثناء بناء الـBM25، فده الشكل الكامل الأنسب للكود.




from langchain_chroma import Chroma

from config import CHROMA_DIRECTORY, RAG_COLLECTION_NAME
from rag.embeddings import get_embeddings


def create_vectorstore():

    vectorstore = Chroma(
        collection_name=RAG_COLLECTION_NAME,
        embedding_function=get_embeddings(),
        persist_directory=CHROMA_DIRECTORY,
        collection_metadata={
            "hnsw:space": "cosine"
        },
    )

    return vectorstore  #بيرجع Chroma Vector Store object من LangChain: