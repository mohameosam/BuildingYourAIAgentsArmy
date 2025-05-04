import time
import requests
import sqlite3
from datetime import datetime

class WeatherAgent:
    def __init__(self, api_key, city="New York"):
        self.api_key = api_key
        self.city = city
        self.temp_limit = 32  # Freeze warning (°F)
        self.conn = sqlite3.connect("weather.db")
        self.create_table()

    def create_table(self):
        # Set up SQLite table
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                city TEXT,
                temp REAL,
                time TEXT,
                message TEXT
            )
        """)
        self.conn.commit()

    def see(self):
        # Get real weather from OpenWeatherMap
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={self.city}&appid={self.api_key}&units=imperial"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            temp = data["main"]["temp"]
            return temp
        except requests.RequestException:
            print("Network error, retrying...")
            return None

    def think(self, temp):
        # Decide if it’s too cold, using MCP to fetch weather data
        if temp is None:
            return False, "No data"
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        is_cold = temp < self.temp_limit
        message = f"{self.city} at {current_time}: {temp}°F"
        return is_cold, message

    def act(self, is_cold, message):
        # Save to SQLite and print alert
        cursor = self.conn.cursor()
        if is_cold:
            alert = f"Freezing alert: {message}"
            print(alert)
            cursor.execute(
                "INSERT INTO alerts (city, temp, time, message) VALUES (?, ?, ?, ?)",
                (self.city, message.split(":")[1].split("°F")[0].strip(), message.split(":")[0].split("at")[1].strip(), alert)
            )
        else:
            print(f"Okay: {message}")
            cursor.execute(
                "INSERT INTO alerts (city, temp, time, message) VALUES (?, ?, ?, ?)",
                (self.city, message.split(":")[1].split("°F")[0].strip(), message.split(":")[0].split("at")[1].strip(), "Okay")
            )
        self.conn.commit()

    def run(self):
        print(f"Weather agent watching {self.city}...")
        while True:
            temp = self.see()
            is_cold, message = self.think(temp)
            self.act(is_cold, message)
            time.sleep(60)  # Check every minute

if __name__ == "__main__":
    # Replace with your OpenWeatherMap API key
    api_key = "your_api_key_here"
    agent = WeatherAgent(api_key=api_key, city="New York")
    agent.run()


    
# Run the script from bash:
#
# python weather_advanced.py