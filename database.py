import sqlite3
from datetime import datetime
import os


# --------------------------------------------------
# Database location
# --------------------------------------------------

DATABASE_FILE = "data/pump_data.db"


# --------------------------------------------------
# Create database folder if it does not exist
# --------------------------------------------------

os.makedirs("data", exist_ok=True)


# --------------------------------------------------
# Create database and table
# --------------------------------------------------

def create_database():

    connection = sqlite3.connect(DATABASE_FILE)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sensor_readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            machine_id TEXT NOT NULL,
            temperature REAL,
            vibration_rms REAL,
            current REAL,
            voltage REAL,
            power REAL,
            energy REAL,
            rpm REAL,
            pressure REAL
        )
    """)

    connection.commit()
    connection.close()


# --------------------------------------------------
# Save one sensor reading
# --------------------------------------------------

def save_sensor_data(data):

    connection = sqlite3.connect(DATABASE_FILE)

    cursor = connection.cursor()

    timestamp = datetime.now().isoformat()

    cursor.execute("""
        INSERT INTO sensor_readings (
            timestamp,
            machine_id,
            temperature,
            vibration_rms,
            current,
            voltage,
            power,
            energy,
            rpm,
            pressure
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        timestamp,
        data.machine_id,
        data.temperature,
        data.vibration_rms,
        data.current,
        data.voltage,
        data.power,
        data.energy,
        data.rpm,
        data.pressure
    ))

    connection.commit()
    connection.close()

    return timestamp


# --------------------------------------------------
# Get recent readings
# --------------------------------------------------

def get_recent_readings(limit=20):

    connection = sqlite3.connect(DATABASE_FILE)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            timestamp,
            machine_id,
            temperature,
            vibration_rms,
            current,
            voltage,
            power,
            energy,
            rpm,
            pressure
        FROM sensor_readings
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()

    connection.close()

    return rows