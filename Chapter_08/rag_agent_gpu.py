import torch
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import logging

logging.basicConfig(filename="rag_gpu.log", level=logging.INFO)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def initialize_rag_gpu(documents):
    model = SentenceTransformer("all-MiniLM-L6-v2").to(device)
    embeddings = model.encode(documents, convert_to_tensor=True, device=device)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings.cpu().numpy())
    return model, index

def query_rag_gpu(query, model, index, documents, top_k=1):
    query_embedding = model.encode([query], convert_to_tensor=True, device=device)
    distances, indices = index.search(query_embedding.cpu().numpy(), top_k)
    results = [documents[idx] for idx in indices[0]]
    logging.info(f"GPU RAG query: {query}")
    return results

