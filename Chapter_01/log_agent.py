import time
from random import randint

class LogMonitorAgent:
    def __init__(self, limit=10):
        self.limit = limit  # Max errors allowed
        self.logs = []      # Holds recent data

    def see(self):
        # Pretend to read logs—random numbers for now
        errors = randint(0, 20)
        self.logs.append(errors)
        if len(self.logs) > 5:  # Keep last 5
            self.logs.pop(0)
        return errors

    def think(self, data):
        # Decide if errors are too high
        return data > self.limit

    def act(self, decision):
        if decision:
            print(f"Warning: Too many errors ({self.logs[-1]})!")
        else:
            print("All good.")

    def run(self):
        print("Agent starting...")
        while True:
            data = self.see()
            choice = self.think(data)
            self.act(choice)
            time.sleep(1)  # Wait 1 second

# Start it
if __name__ == "__main__":
    agent = LogMonitorAgent(limit=10)
    agent.run()

    
# Run the script from bash:
#
# python log_agent.py