from langchain_chroma import Chroma

from backend.rag.embeddings import get_embeddings


def get_retriever():

    embeddings = get_embeddings()

    vector_store = Chroma(
        persist_directory="data/chroma",
        embedding_function=embeddings
    )

    retriever = vector_store.as_retriever(
        search_kwargs={"k": 4}
    )

    return retriever