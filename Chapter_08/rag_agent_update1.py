import numpy as np

session = ort.InferenceSession("llama3_quantized.onnx")
def query_rag(item_id):
    inputs = tokenizer(f"Details for item {item_id}", return_tensors="np")["input_ids"]
    outputs = session.run(None, {"input": inputs})[0]
    return tokenizer.decode(outputs[0], skip_special_tokens=True)
