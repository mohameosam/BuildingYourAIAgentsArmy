# Before you run this script make sure that the weather.db exists
# if it does not exist run the following script:
# python create_sqlite_database.py
import sqlite3
conn = sqlite3.connect("weather.db")
cursor = conn.cursor()
cursor.execute("SELECT * FROM alerts")
print(cursor.fetchall())
conn.close()


    
# Run the script from bash:
#
# python check_weather_db.py