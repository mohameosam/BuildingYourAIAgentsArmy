import time
from random import randint

class WeatherAgent:
    def __init__(self, temp_limit=32):
        self.temp_limit = temp_limit  # Freeze warning at 32°F
        self.recent_temps = []       # Store last 5 temps

    def see(self):
        # Fake sensor: random temp between 20-80°F
        temp = randint(20, 80)
        self.recent_temps.append(temp)
        if len(self.recent_temps) > 5:
            self.recent_temps.pop(0)
        return temp

    def think(self, temp):
        # Decide if it’s too cold
        return temp < self.temp_limit

    def act(self, is_cold):
        if is_cold:
            print(f"Warning: Freezing at {self.recent_temps[-1]}°F!")
        else:
            print(f"Temperature okay: {self.recent_temps[-1]}°F.")

    def run(self):
        print("Weather agent starting...")
        while True:
            temp = self.see()
            decision = self.think(temp)
            self.act(decision)
            time.sleep(2)  # Check every 2 seconds

if __name__ == "__main__":
    agent = WeatherAgent()
    agent.run()


    
# Run the script from bash:
#
# python weather_basic.py