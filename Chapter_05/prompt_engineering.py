# File: prompt_engineering.py
# Chapter 5: Advanced AI Agent Techniques
# This script demonstrates prompt engineering for better model responses.

# Import LangChain
from langchain.llms import Ollama

# Initialize model
llm = Ollama(model="llama3")

# Function to engineer a prompt
def engineer_prompt(task, context=""):
    prompt = f"Given the context: {context}\nPerform this task with precision: {task}"
    return prompt

# Query function
def query_with_prompt(task, context=""):
    prompt = engineer_prompt(task, context)
    return llm(prompt)

# Example usage
if __name__ == "__main__":
    task = "Summarize the benefits of AI in business."
    context = "AI improves efficiency and reduces costs."
    response = query_with_prompt(task, context)
    print("Prompt Engineered Response:", response)