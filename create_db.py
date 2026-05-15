from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

def create_db():
    print("📖 Loading encyclopedia PDF (481 pages)...")
    loader = PyPDFLoader("encyclopedia.pdf")
    docs = loader.load()
    print(f"✅ Loaded {len(docs)} pages.")

    print("✂️  Splitting into chunks...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(docs)
    print(f"✅ Created {len(chunks)} chunks.")

    print("🔢 Embedding into ChromaDB (this takes a few minutes)...")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    Chroma.from_documents(
        chunks,
        embeddings,
        persist_directory="./chroma_db"
    )
    print("✅ Vector database saved to ./chroma_db — done!")

if __name__ == "__main__":
    create_db()