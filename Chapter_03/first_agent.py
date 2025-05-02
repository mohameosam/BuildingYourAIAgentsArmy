# File: first_agent.py
# Chapter 3: Building Your First AI Agent
# This script builds a simple AI agent to automate email responses.

# Import LangChain and email libraries
from langchain import LLMChain
from langchain.llms import Ollama
import smtplib

# Initialize the language model
llm = Ollama(model="llama3")

# Create an email response agent
def email_response_agent():
    chain = LLMChain(llm=llm, prompt="Draft a professional email response to: {input}")
    return chain

# Send email function
def send_email(response, recipient):
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login("your_email@gmail.com", "your_password")
        server.sendmail("your_email@gmail.com", recipient, response)

# Example usage
if __name__ == "__main__":
    agent = email_response_agent()
    email_content = agent.run("Request for project update.")
    send_email(email_content, "recipient@example.com")