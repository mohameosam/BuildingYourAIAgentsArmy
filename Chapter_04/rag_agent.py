# File: rag_agent.py
# Chapter 4: Retrieval-Augmented Generation (RAG) in AI Agents
# This script implements a RAG agent using FAISS and Sentence-Transformers.

# Import necessary libraries
from langchain.llms import Ollama
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Initialize models and index
llm = Ollama(model="llama3")
embedder = SentenceTransformer('all-MiniLM-L6-v2')
index = faiss.IndexFlatL2(384)  # 384-dim embeddings

# Function to build RAG agent
def build_rag_agent(documents):
    embeddings = embedder.encode(documents)
    index.add(np.array(embeddings))
    return index

# Query function
def query_rag(query, documents, index):
    query_embedding = embedder.encode([query])
    D, I = index.search(np.array(query_embedding), k=1)
    context = documents[I[0][0]]
    prompt = f"Answer using this context: {context}\nQuery: {query}"
    return llm(prompt)

# Example usage
if __name__ == "__main__":
    docs = ["AI agents automate tasks.", "RAG improves accuracy."]
    rag_index = build_rag_agent(docs)
    response = query_rag("What does RAG do?", docs, rag_index)
    print("RAG Response:", response)