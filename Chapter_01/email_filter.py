import time
from random import choice

class EmailFilterAgent:
    def __init__(self):
        self.urgent_words = ["urgent", "emergency", "asap"]  # Words to flag
        self.emails = []  # Store recent emails

    def see(self):
        # Simulate fetching an email subject
        subjects = [
            "Meeting tomorrow",
            "Urgent: Action needed ASAP",
            "Lunch plans",
            "Emergency: System down",
            "Weekly report"
        ]
        subject = choice(subjects)  # Pick one randomly
        self.emails.append(subject)
        if len(self.emails) > 5:  # Keep last 5
            self.emails.pop(0)
        return subject

    def think(self, subject):
        # Check if subject has urgent words
        subject = subject.lower()
        return any(word in subject for word in self.urgent_words)

    def act(self, is_urgent):
        if is_urgent:
            print(f"Alert: Urgent email detected - '{self.emails[-1]}'!")
        else:
            print(f"Email okay: '{self.emails[-1]}'.")

    def run(self):
        print("Email filter agent starting...")
        while True:
            subject = self.see()
            is_urgent = self.think(subject)
            self.act(is_urgent)
            time.sleep(2)  # Check every 2 seconds

# Start it
if __name__ == "__main__":
    agent = EmailFilterAgent()
    agent.run()



# Run the script from bash:
#
# python email_filter.py