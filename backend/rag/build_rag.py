from backend.rag.document_loader import load_documents
from backend.rag.text_splitter import split_documents
from backend.rag.vector_store import create_vector_store


PDF_FOLDER = "data/documents/java"


def build_rag():

    print("Loading documents...")

    documents = load_documents(PDF_FOLDER)

    print(f"Documents loaded: {len(documents)}")

    print("Splitting documents...")

    chunks = split_documents(documents)

    print(f"Chunks created: {len(chunks)}")

    print("Creating vector database...")

    create_vector_store(chunks)

    print("RAG knowledge base created successfully!")


if __name__ == "__main__":
    build_rag()