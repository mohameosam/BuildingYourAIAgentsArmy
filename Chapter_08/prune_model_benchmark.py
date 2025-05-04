import time
from transformers import pipeline

original = pipeline("text-generation", model="llama3")
pruned = pipeline("text-generation", model="pruned_llama3")
input_text = "Details for item ABC"

start = time.time()
original(input_text, max_length=50)
original_time = time.time() - start

start = time.time()
pruned(input_text, max_length=50)
pruned_time = time.time() - start

print(f"Original: {original_time:.2f}s, Pruned: {pruned_time:.2f}s")
