import sqlite3
from datetime import datetime, timedelta
import random


def create_database(db_path='weather.db'):
    """Create the database schema with empty tables"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create alerts table (singular as requested)
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS alerts
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       city
                       TEXT
                       NOT
                       NULL,
                       temp
                       REAL
                       NOT
                       NULL,
                       time
                       TIMESTAMP
                       NOT
                       NULL
                       DEFAULT
                       CURRENT_TIMESTAMP,
                       message
                       TEXT,
                       status
                       TEXT
                       DEFAULT
                       'active'
                       CHECK (
                       status
                       IN
                   (
                       'active',
                       'resolved',
                       'acknowledged'
                   )),
                       severity TEXT CHECK
                   (
                       severity
                       IN
                   (
                       'low',
                       'medium',
                       'high',
                       'critical'
                   ))
                       )
                   ''')

    # Create indexes
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_alert_city ON alerts(city)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_alert_time ON alerts(time)')

    conn.commit()
    conn.close()
    print(f"Database schema created at {db_path} with 'alerts' table")


def populate_database(db_path='weather.db', num_alerts=50):
    """Populate the database with realistic dummy data"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Data generation configuration
    cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix',
              'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose']

    alert_messages = {
        'high': ['Heat wave warning', 'Extreme temperature alert', 'Dangerous heat levels'],
        'medium': ['Temperature advisory', 'Weather alert', 'Unusual temperatures expected'],
        'low': ['Mild weather notice', 'Temperature fluctuation', 'Seasonal weather pattern'],
        'critical': ['EMERGENCY: Extreme weather', 'DANGER: Life-threatening temperatures',
                     'URGENT: Evacuation advisory']
    }

    # Insert dummy alerts
    for _ in range(num_alerts):
        city = random.choice(cities)
        severity = random.choice(['low', 'medium', 'high', 'critical'])

        # Generate appropriate temperature based on severity
        if severity == 'critical':
            temp = random.uniform(100, 120) if random.random() > 0.5 else random.uniform(-20, 0)
        elif severity == 'high':
            temp = random.uniform(90, 100) if random.random() > 0.5 else random.uniform(0, 10)
        elif severity == 'medium':
            temp = random.uniform(80, 90) if random.random() > 0.5 else random.uniform(10, 20)
        else:
            temp = random.uniform(60, 80) if random.random() > 0.5 else random.uniform(20, 40)

        message = random.choice(alert_messages[severity])
        time = datetime.now() - timedelta(
            days=random.randint(0, 30),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )
        status = random.choices(
            ['active', 'resolved', 'acknowledged'],
            weights=[0.6, 0.3, 0.1]
        )[0]

        cursor.execute('''
                       INSERT INTO alerts (city, temp, time, message, severity, status)
                       VALUES (?, ?, ?, ?, ?, ?)
                       ''', (city, round(temp, 1), time, message, severity, status))

    conn.commit()
    conn.close()
    print(f"Database populated with {num_alerts} sample alerts in 'alerts' table")


if __name__ == '__main__':
    # Example usage
    create_database()
    populate_database(num_alerts=50)