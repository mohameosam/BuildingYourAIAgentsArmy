from langchain.llms import Ollama
from sentence_transformers import SentenceTransformer

# Test Ollama
llm = Ollama(model="llama3")
print(llm("What is RAG?"))

# Test embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode("Test sentence")
print(embeddings.shape)  # Should be (384,)



# Run the script from bash:
#
# python test_rag.py