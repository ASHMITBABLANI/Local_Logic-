from flask import Flask, render_template, request, jsonify
from langchain_ollama.llms import OllamaLLM 
from langchain_core.prompts import ChatPromptTemplate
from PyPDF2 import PdfReader
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import os
app = Flask(__name__)
embedding = OllamaEmbeddings(model="mxbai-embed-large")
store = Chroma(collection_name="Rag_Data", embedding_function=embedding)
retriever = store.as_retriever(search_kwargs={"k": 5})
model = OllamaLLM(model="gemma2:2b")
message_template = "You are a personal assistant helping by giving a summary of the document uploaded based on context: {content} and user question: {question}"
prompt = ChatPromptTemplate.from_template(message_template)
chain = prompt | model
@app.route("/")
def index():
    return render_template("index.html")
@app.route("/upload", methods=["POST"])
def upload_files():
    if "files" not in request.files:
        return jsonify({"error": "No files found"}), 400
    files = request.files.getlist("files")
    all_docs = []
    for file in files:
        if file.filename.endswith(".pdf"):
            reader = PdfReader(file)
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    all_docs.append(Document(page_content=text))   
    if all_docs:
        store.add_documents(all_docs)
        return jsonify({"message": f"Successfully processed {len(files)} PDF(s)!"})
    
    return jsonify({"error": "No text extracted from files."}), 400

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    question = data.get("question", "")
    
    if not question:
        return jsonify({"response": "Please enter a valid question."})
        
    if question.lower() in ["q", "quit"]:
        return jsonify({"response": "Hope you feel better!"})
        
    try:
        content = retriever.invoke(question)
        response = chain.invoke({"content": content, "question": question})
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"response": f"Error communicating with local LLM: {str(e)}"})

if __name__ == "__main__":
    app.run(port=5000)