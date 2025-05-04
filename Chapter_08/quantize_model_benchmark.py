import time
import numpy as np

session = ort.InferenceSession("llama3_quantized.onnx")
inputs = tokenizer("Details for item ABC", return_tensors="np")["input_ids"]
start = time.time()
session.run(None, {"input": inputs})
print(f"Quantized inference: {time.time() - start:.2f}s")
