from flask import Flask, request, jsonify, send_from_directory
from qa_chain import load_db, setup_qa_chain
import os

app = Flask(__name__, static_folder="static")

print("⏳ Loading vector database...")
vector_db = load_db()
chain, retriever = setup_qa_chain(vector_db)
print("𓂀 EgyptBot is ready!")

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    question = data.get("question", "").strip()
    if not question:
        return jsonify({"error": "Empty question"}), 400
    try:
        answer = chain.invoke(question)
        docs = retriever.invoke(question)
        pages = sorted(set(
            doc.metadata.get("page", "?") for doc in docs
        )) if docs else []
        return jsonify({"answer": answer, "pages": pages})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)