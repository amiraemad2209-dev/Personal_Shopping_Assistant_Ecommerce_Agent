
from langchain_docling import DoclingLoader
from langchain_docling.loader import ExportType


def load_document(file_path: str):
    """
    Load a document using Docling
    and return LangChain Documents.
    """

    loader = DoclingLoader(
        file_path=file_path,
        export_type=ExportType.MARKDOWN,
    )

    documents = loader.load()

    return documents

