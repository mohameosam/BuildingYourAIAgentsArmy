# File: basic_agent.py
# Chapter 1: Introduction to AI Agents and Open-Source Tools
# This script demonstrates a basic AI agent using LangChain to respond to user queries.

# Import LangChain for building the agent
from langchain import LLMChain
from langchain.llms import Ollama

# Initialize the language model with Ollama
llm = Ollama(model="llama3")

# Define a simple agent to respond to user input
def create_basic_agent():
    # Create a chain for conversational responses
    chain = LLMChain(llm=llm, prompt="You are a helpful AI assistant. Respond to: {input}")
    return chain

# Example usage
if __name__ == "__main__":
    agent = create_basic_agent()
    response = agent.run("What is an AI agent?")
    print("Agent Response:", response)