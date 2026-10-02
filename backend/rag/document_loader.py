from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader


def load_documents(folder_path):
    documents = []

    folder = Path(folder_path)

    pdf_files = list(folder.rglob("*.pdf"))

    for pdf_file in pdf_files:
        try:
            loader = PyPDFLoader(str(pdf_file))
            pdf_documents = loader.load()
            documents.extend(pdf_documents)
        except Exception as e:
            print(f"Could not load {pdf_file}: {e}")

    return documents