from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader


def load_documents(folder_path):

    documents = []

    folder = Path(folder_path)

    pdf_files = list(folder.glob("*.pdf"))

    for pdf_file in pdf_files:

        loader = PyPDFLoader(str(pdf_file))

        pdf_documents = loader.load()

        documents.extend(pdf_documents)

    return documents