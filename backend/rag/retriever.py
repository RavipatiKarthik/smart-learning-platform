from pathlib import Path

from langchain_chroma import Chroma

from backend.rag.embeddings import get_embeddings
from backend.rag.build_rag import build_rag


CHROMA_PATH = Path("data/chroma")


def get_retriever():

    embeddings = get_embeddings()

    if not CHROMA_PATH.exists() or not any(CHROMA_PATH.iterdir()):

        print("RAG database not found.")
        print("Building RAG knowledge base...")

        build_rag()

    vector_store = Chroma(
        persist_directory=str(CHROMA_PATH),
        embedding_function=embeddings
    )

    retriever = vector_store.as_retriever(
        search_kwargs={"k": 4}
    )

    return retriever