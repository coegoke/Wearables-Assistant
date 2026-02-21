"""Database setup and initialization for wearables data."""
import sqlite3
from datetime import datetime, timedelta
import random


def create_database():
    """Create and populate the wearables database with sample data."""
    conn = sqlite3.connect('wearables.db')
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER,
            gender TEXT,
            height_cm REAL,
            weight_kg REAL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS devices (
            device_id INTEGER PRIMARY KEY,
            user_id INTEGER,
            device_type TEXT NOT NULL,
            brand TEXT NOT NULL,
            model TEXT NOT NULL,
            purchase_date TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_metrics (
            metric_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            date TEXT NOT NULL,
            steps INTEGER,
            distance_km REAL,
            calories_burned INTEGER,
            active_minutes INTEGER,
            floors_climbed INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS heart_rate (
            hr_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            timestamp TEXT NOT NULL,
            heart_rate INTEGER,
            resting_heart_rate INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sleep_data (
            sleep_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            date TEXT NOT NULL,
            total_sleep_hours REAL,
            deep_sleep_hours REAL,
            light_sleep_hours REAL,
            rem_sleep_hours REAL,
            awake_hours REAL,
            sleep_score INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS activities (
            activity_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            date TEXT NOT NULL,
            activity_type TEXT NOT NULL,
            duration_minutes INTEGER,
            calories INTEGER,
            average_heart_rate INTEGER,
            max_heart_rate INTEGER,
            distance_km REAL,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    ''')
    
    # Insert sample user
    cursor.execute('''
        INSERT OR REPLACE INTO users (user_id, name, age, gender, height_cm, weight_kg)
        VALUES (1, 'John Doe', 32, 'Male', 175, 75)
    ''')
    
    # Insert sample device
    cursor.execute('''
        INSERT OR REPLACE INTO devices (device_id, user_id, device_type, brand, model, purchase_date)
        VALUES (1, 1, 'Smartwatch', 'Apple', 'Apple Watch Series 9', '2024-01-15')
    ''')
    
    # Generate sample data for the last 30 days
    base_date = datetime.now() - timedelta(days=30)
    
    for i in range(30):
        current_date = base_date + timedelta(days=i)
        date_str = current_date.strftime('%Y-%m-%d')
        
        # Daily metrics
        steps = random.randint(5000, 15000)
        cursor.execute('''
            INSERT INTO daily_metrics (user_id, date, steps, distance_km, calories_burned, active_minutes, floors_climbed)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (1, date_str, steps, round(steps * 0.0008, 2), random.randint(1800, 2800), 
              random.randint(30, 120), random.randint(5, 25)))
        
        # Sleep data
        total_sleep = round(random.uniform(6.0, 9.0), 2)
        deep_sleep = round(total_sleep * random.uniform(0.15, 0.25), 2)
        rem_sleep = round(total_sleep * random.uniform(0.20, 0.30), 2)
        light_sleep = round(total_sleep - deep_sleep - rem_sleep - random.uniform(0.1, 0.5), 2)
        awake = round(total_sleep * random.uniform(0.05, 0.10), 2)
        
        cursor.execute('''
            INSERT INTO sleep_data (user_id, date, total_sleep_hours, deep_sleep_hours, 
                                   light_sleep_hours, rem_sleep_hours, awake_hours, sleep_score)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (1, date_str, total_sleep, deep_sleep, light_sleep, rem_sleep, awake, 
              random.randint(60, 95)))
        
        # Heart rate data (sample throughout the day)
        for hour in range(0, 24, 2):
            timestamp = current_date.replace(hour=hour, minute=random.randint(0, 59))
            hr = random.randint(60, 120)
            cursor.execute('''
                INSERT INTO heart_rate (user_id, timestamp, heart_rate, resting_heart_rate)
                VALUES (?, ?, ?, ?)
            ''', (1, timestamp.strftime('%Y-%m-%d %H:%M:%S'), hr, random.randint(55, 65)))
        
        # Activities (random 2-3 times per week)
        if random.random() < 0.4:
            activity_types = ['Running', 'Cycling', 'Swimming', 'Walking', 'Yoga', 'Gym Workout']
            activity = random.choice(activity_types)
            duration = random.randint(20, 90)
            
            cursor.execute('''
                INSERT INTO activities (user_id, date, activity_type, duration_minutes, 
                                       calories, average_heart_rate, max_heart_rate, distance_km)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (1, date_str, activity, duration, random.randint(200, 800),
                  random.randint(110, 150), random.randint(150, 180), 
                  round(random.uniform(2, 15), 2) if activity in ['Running', 'Cycling', 'Walking'] else 0))
    
    conn.commit()
    conn.close()
    print("Database created and populated successfully!")


if __name__ == '__main__':
    create_database()
