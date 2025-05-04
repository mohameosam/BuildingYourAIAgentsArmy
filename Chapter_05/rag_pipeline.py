from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.llms import Ollama
from langchain.chains import RetrievalQA
from sentence_transformers import SentenceTransformer

# Load PDF
loader = PyPDFLoader("data/tech_trends.pdf")
documents = loader.load()

# Split into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
texts = text_splitter.split_documents(documents)

# Create embeddings
embedder = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = [embedder.encode(doc.page_content) for doc in texts]

# Build FAISS index
vector_store = FAISS.from_texts([doc.page_content for doc in texts], embedder.encode)

# Initialize LLM
llm = Ollama(model="llama3")

# Create RAG chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vector_store.as_retriever(search_kwargs={"k": 3})
)

# Query
query = "What are the top tech trends for 2025?"
response = qa_chain.run(query)
print(response)



# Run the script from bash:
#
# python rag_pipeline.py