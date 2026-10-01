from langchain_chroma import Chroma

from backend.rag.embeddings import get_embeddings


def create_vector_store(chunks):

    embeddings = get_embeddings()

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="data/chroma"
    )

    return vector_store