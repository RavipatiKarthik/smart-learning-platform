from backend.rag.retriever import get_retriever


retriever = get_retriever()

query = input("Ask a question: ")

documents = retriever.invoke(query)

print("\nRelevant Knowledge:\n")

for i, document in enumerate(documents, start=1):
    print(f"--- Result {i} ---")
    print(document.page_content)
    print()