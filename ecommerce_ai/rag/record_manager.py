


#ده مسؤول عن tracking للـdocuments اللي دخلت الـvectorstore.

from langchain_classic.indexes import SQLRecordManager


def create_record_manager():

    namespace = "chroma/my_rag_collection"

    record_manager = SQLRecordManager(
        namespace=namespace,
        db_url="sqlite:///record_manager_cache.sql",
    )

    record_manager.create_schema()

    return record_manager