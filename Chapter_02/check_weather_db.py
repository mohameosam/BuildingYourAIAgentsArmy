import sqlite3
conn = sqlite3.connect("weather.db")
cursor = conn.cursor()
cursor.execute("SELECT * FROM alerts")
print(cursor.fetchall())
conn.close()


    
# Run the script from bash:
#
# python check_weather_db.py