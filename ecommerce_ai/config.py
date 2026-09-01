

# ===============================================================================#
# ============================= configurations ==================================#
# ===============================================================================#


import os
from pathlib import Path


from dotenv import load_dotenv


load_dotenv()

GROQ_MODEL = "openai/gpt-oss-20b"
TEMPERATURE = 0

BASE_DIR = Path(__file__).resolve().parent
MEMORY_DATABASE = "sqlite:///ecommerce_memory.db"
MAX_ITERATIONS = 3


CHROMA_DIRECTORY = os.getenv(
    "CHROMA_DIRECTORY",
    "./chroma_db"
)

RAG_COLLECTION_NAME = os.getenv(
    "RAG_COLLECTION_NAME",
    "my_rag_collection"
)