import time
import json
import random
from azure.iot.device import IoTHubDeviceClient
from datetime import datetime

# Azure IoT Hub connection string
CONNECTION_STRING = "HostName=rideaucanalIOT.azure-devices.net;DeviceId=canalsensor;SharedAccessKey=bfaR0bldfD43flG8DYyT9oTxp1Vq35YLEmkzFMALh30="

def generate_sensor_data(location):
    return {
        "location": location,
        "iceThickness": round(random.uniform(20, 30), 1),  # 20-30 cm
        "surfaceTemperature": round(random.uniform(-5, 0), 1),  # -5 to 0°C
        "snowAccumulation": round(random.uniform(0, 10), 1),  # 0-10 cm
        "externalTemperature": round(random.uniform(-10, 0), 1),  # -10 to 0°C
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

def run_simulation():
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    locations = ["Dow's Lake", "Fifth Avenue", "NAC"]
    
    while True:
        for location in locations:
            data = generate_sensor_data(location)
            message = json.dumps(data)
            client.send_message(message)
            print(f"Sent: {message}")
        time.sleep(10)  # Every 10 seconds

if __name__ == "__main__":
    run_simulation()