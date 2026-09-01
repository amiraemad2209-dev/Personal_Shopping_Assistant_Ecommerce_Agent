

 
# هنا بنربط الـchunks بالـvectorstore والـrecord manager.

from langchain_core.indexing import index

from rag.vectorstore import create_vectorstore
from rag.record_manager import create_record_manager


def add_documents(documents):

    vectorstore = create_vectorstore()
    record_manager = create_record_manager()

    result = index(
        docs_source=documents,
        record_manager=record_manager,
        vector_store=vectorstore,
        cleanup="incremental",
        source_id_key="source",
    )

    return result