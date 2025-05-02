# File: setup_environment.py
# Chapter 2: Setting Up Your Environment
# This script sets up the environment with necessary tools like Redis and RabbitMQ.

# Import libraries for setup
import subprocess
import sys

# Function to install Redis
def install_redis():
    print("Installing Redis...")
    subprocess.run(["sudo", "apt-get", "install", "-y", "redis-server"])
    subprocess.run(["sudo", "systemctl", "start", "redis"])

# Function to install RabbitMQ
def install_rabbitmq():
    print("Installing RabbitMQ...")
    subprocess.run(["sudo", "apt-get", "install", "-y", "rabbitmq-server"])
    subprocess.run(["sudo", "systemctl", "enable", "rabbitmq-server"])

# Main setup function
def setup_environment():
    install_redis()
    install_rabbitmq()
    print("Environment setup complete.")

# Run setup
if __name__ == "__main__":
    setup_environment()