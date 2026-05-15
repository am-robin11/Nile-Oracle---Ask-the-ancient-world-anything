import os
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

load_dotenv()

def load_db():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    return Chroma(
        persist_directory="./chroma_db",
        embedding_function=embeddings
    )

def setup_qa_chain(vector_db):
    llm = ChatGroq(
        temperature=0,
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama-3.3-70b-versatile"
    )

    retriever = vector_db.as_retriever(search_kwargs={"k": 4})

    prompt = ChatPromptTemplate.from_template("""You are EgyptBot, an expert \
guide to Ancient Egyptian history, civilization, and culture. Use the \
encyclopedia excerpts below to answer the question. If the excerpts don't \
cover it, say so and use your general knowledge, clearly noting you are \
doing so. Be engaging, accurate, and bring the ancient world to life.

Encyclopedia excerpts:
{context}

Question: {question}

Answer:""")

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain, retriever