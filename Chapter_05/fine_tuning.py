# File: fine_tuning.py
# Chapter 5: Advanced AI Agent Techniques
# This script demonstrates fine-tuning a model for a specific task.

# Import libraries
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# Load model and tokenizer
model = AutoModelForCausalLM.from_pretrained("gpt2")
tokenizer = AutoTokenizer.from_pretrained("gpt2")

# Fine-tuning function
def fine_tune_model(data):
    inputs = tokenizer(data, return_tensors="pt", truncation=True, padding=True)
    outputs = model(**inputs, labels=inputs["input_ids"])
    loss = outputs.loss
    loss.backward()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-5)
    optimizer.step()
    return model

# Example usage
if __name__ == "__main__":
    data = ["Automate business tasks with AI."]
    fine_tuned_model = fine_tune_model(data)
    print("Model fine-tuned.")