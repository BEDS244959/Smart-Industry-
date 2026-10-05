from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

from database import (
    create_database,
    save_sensor_data,
    get_recent_readings
)


# --------------------------------------------------
# Create FastAPI application
# --------------------------------------------------

app = FastAPI(
    title="Smart Industry AI Sensor Server",
    description="Real-time industrial pump sensor data server",
    version="1.0"
)


# --------------------------------------------------
# Create database when server starts
# --------------------------------------------------

create_database()


# --------------------------------------------------
# Sensor data format
# --------------------------------------------------

class SensorData(BaseModel):

    machine_id: str
    temperature: float
    vibration_rms: float
    current: float
    voltage: float
    power: float
    energy: float
    rpm: float
    pressure: float


# --------------------------------------------------
# Home page
# --------------------------------------------------

@app.get("/")
def home():

    return {
        "status": "online",
        "message": "Smart Industry AI Sensor Server is running",
        "time": datetime.now().isoformat()
    }


# --------------------------------------------------
# Receive sensor data
# --------------------------------------------------

@app.post("/sensor-data")
def receive_sensor_data(data: SensorData):

    timestamp = save_sensor_data(data)

    print("\n====================================")
    print("NEW SENSOR READING")
    print("====================================")

    print(f"Time        : {timestamp}")
    print(f"Machine ID  : {data.machine_id}")
    print(f"Temperature : {data.temperature} °C")
    print(f"Vibration   : {data.vibration_rms}")
    print(f"Current     : {data.current} A")
    print(f"Voltage     : {data.voltage} V")
    print(f"Power       : {data.power} W")
    print(f"Energy      : {data.energy} kWh")
    print(f"RPM         : {data.rpm}")
    print(f"Pressure    : {data.pressure} bar")

    print("====================================\n")

    return {
        "status": "success",
        "message": "Sensor data received and stored",
        "machine_id": data.machine_id,
        "saved_at": timestamp,
        "data": data.model_dump()
    }


# --------------------------------------------------
# Get recent readings
# --------------------------------------------------

@app.get("/readings")
def recent_readings(limit: int = 20):

    rows = get_recent_readings(limit)

    readings = []

    for row in rows:

        readings.append({
            "timestamp": row[0],
            "machine_id": row[1],
            "temperature": row[2],
            "vibration_rms": row[3],
            "current": row[4],
            "voltage": row[5],
            "power": row[6],
            "energy": row[7],
            "rpm": row[8],
            "pressure": row[9]
        })

    return {
        "count": len(readings),
        "readings": readings
    }