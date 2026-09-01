
from langchain_huggingface import HuggingFaceEmbeddings


def get_embeddings():

    encode_kwargs = {
        "batch_size": 100,
        "normalize_embeddings": True,
    }

    model_name = "sentence-transformers/all-MiniLM-L6-v2"

    embeddings = HuggingFaceEmbeddings(
        model_name=model_name,
        encode_kwargs=encode_kwargs,
        show_progress=False,
    )

    return embeddings

