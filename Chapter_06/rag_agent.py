from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.llms import Ollama
from langchain.chains import RetrievalQA
from sentence_transformers import SentenceTransformer
import requests
import sqlite3
from datetime import datetime, timedelta
import logging

logging.basicConfig(filename="rag.log", level=logging.INFO)

# Load catalog
loader = PyPDFLoader("data/products.pdf")
documents = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
texts = text_splitter.split_documents(documents)

# Embeddings
embedder = SentenceTransformer("all-MiniLM-L6-v2")
vector_store = FAISS.from_texts([doc.page_content for doc in texts], embedder.encode)

# LLM
llm = Ollama(model="llama3")

# RAG chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vector_store.as_retriever(search_kwargs={"k": 3})
)

# CAG cache
def get_cached_product(product):
    conn = sqlite3.connect("mas_cache.db")
    cursor = conn.cursor()
    cursor.execute("SELECT details FROM product_cache WHERE product = ? AND updated_at > ?",
                  (product, (datetime.now() - timedelta(hours=24)).isoformat()))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def cache_product(product, details):
    conn = sqlite3.connect("mas_cache.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR REPLACE INTO product_cache (product, details, updated_at) VALUES (?, ?, ?)",
        (product, details, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()

def check_inventory(product, quantity, order_id):
    logging.info(f"Checking inventory: {product}, {quantity}, {order_id}")
    cached = get_cached_product(product)
    if cached:
        stock = int(cached.split("in stock")[0].split()[-1]) if "in stock" in cached.lower() else 0
        details = cached
    else:
        query = f"Is {quantity} {product}(s) in stock? Include stock count, price, and specs."
        details = qa_chain.run(query)
        cache_product(product, details)
        stock = int(details.split("in stock")[0].split()[-1]) if "in stock" in details.lower() else 0

    if stock >= quantity:
        status = "confirmed"
    elif stock > 0:
        status = "partial"
        details += f" Only {stock} available."
    else:
        status = "out_of_stock"

    response = requests.post("http://localhost:8000", json={
        "jsonrpc": "2.0",
        "id": 2,
        "method": "update_order",
        "params": {"order_id": order_id, "status": status},
        "api_key": "SECRET_KEY"
    })
    if response.json().get("error"):
        logging.error(f"Error updating order {order_id}: {response.json()['error']}")
    return details

if __name__ == "__main__":
    print(check_inventory("Laptop", 2, "ORD001"))


# Run the script from bash:
#
# python rag_agent.py