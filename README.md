# Final Project Assignment: Real-time Monitoring System for Rideau Canal Skateway


1. **Scenario Description**: 
This project implements a real-time monitoring system for the Rideau Canal Skateway using simulated IoT sensors, Azure IoT Hub, Azure Stream Analytics, and Azure Blob Storage. The system simulates sensor data (ice thickness, surface temperature, snow accumulation, external temperature) from three locations, processes it in real time, and stores aggregated outputs in Blob Storage.

2. **System Architecture**:  
   - Include a clear diagram illustrating the data flow:
     - IoT sensors pushing simulated data to Azure IoT Hub.
     - Azure Stream Analytics processing the incoming data.
     - Processed data being stored in Azure Blob Storage.

3. **Implementation Details**:  
   - **IoT Sensor Simulation**:
     Description:
The IoT sensors are simulated using a Python script that emulates sensors at three Rideau Canal locations: Dow's Lake, Fifth Avenue, and NAC. The script generates data every 10 seconds and sends it to Azure IoT Hub using the Azure IoT Device SDK for Python.

Data Generation:

Locations: Dow's Lake, Fifth Avenue, NAC.
Data Points:
Ice Thickness (cm): Random float between 20 and 30, rounded to one decimal place (e.g., 27.3), simulating safe ice conditions.
Surface Temperature (°C): Random float between -5 and 0, rounded to one decimal place (e.g., -1.2), reflecting cold ice surfaces.
Snow Accumulation (cm): Random float between 0 and 10, rounded to one decimal place (e.g., 8.4), indicating snow cover.
External Temperature (°C): Random float between -10 and 0, rounded to one decimal place (e.g., -4.7), providing weather context.
Timestamp: Current UTC time in ISO 8601 format (e.g., 2024-11-23T12:00:00Z).
Frequency: Data is sent every 10 seconds per location.
Realism: Ranges are based on typical Rideau Canal winter conditions to ensure realistic simulation.
JSON Payload Structure:

json

Copy
{
  "location": "Dow's Lake",
  "iceThickness": 27.3,
  "surfaceTemperature": -1.2,
  "snowAccumulation": 8.4,
  "externalTemperature": -4.7,
  "timestamp": "2024-11-23T12:00:00Z"
}
Script Used (sensor-simulation/simulate_sensors.py):

python

Copy
import time
import json
import random
from azure.iot.device import IoTHubDeviceClient
from datetime import datetime

# Azure IoT Hub device connection string
CONNECTION_STRING = "Your-IoT-Hub-Device-Connection-String"

def generate_sensor_data(location):
    """Generate simulated sensor data for a given location."""
    return {
        "location": location,
        "iceThickness": round(random.uniform(20, 30), 1),  # 20-30 cm
        "surfaceTemperature": round(random.uniform(-5, 0), 1),  # -5 to 0°C
        "snowAccumulation": round(random.uniform(0, 10), 1),  # 0-10 cm
        "externalTemperature": round(random.uniform(-10, 0), 1),  # -10 to 0°C
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

def run_simulation():
    """Simulate sensors and send data to IoT Hub every 10 seconds."""
    try:
        # Initialize IoT Hub client
        client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
        locations = ["Dow's Lake", "Fifth Avenue", "NAC"]
        
        while True:
            for location in locations:
                # Generate and send data
                data = generate_sensor_data(location)
                message = json.dumps(data)
                client.send_message(message)
                print(f"Sent data for {location}: {message}")
            time.sleep(10)  # Wait 10 seconds
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.shutdown()

if __name__ == "__main__":
    run_simulation()
Script Details:

Library: Uses azure-iot-device for IoT Hub communication.
Logic: Loops through locations, generates a JSON payload, serializes it, and sends it to IoT Hub every 10 seconds.
Error Handling: Catches exceptions and ensures client shutdown.
Dependencies: Requires azure-iot-device (install via pip install azure-iot-device).
Execution: Runs indefinitely until stopped, logging sent messages to the console for debugging.
Sending Mechanism:

The script authenticates with IoT Hub using a device-specific connection string.
Messages are sent asynchronously, with the SDK handling retries and connectivity issues
   - **Azure IoT Hub Configuration**:
     - Explain the configuration steps for setting up the IoT Hub, including endpoints and message routing.
   - **Azure Stream Analytics Job**:
     - Describe the job configuration, including input sources, query logic, and output destinations.
     - Provide sample queries used for data processing.
   - **Azure Blob Storage**:
     - Explain how the processed data is organized in Blob Storage (e.g., folder structure, file naming convention).
     - Specify the formats of stored data (JSON/CSV).
![image](https://github.com/user-attachments/assets/6fcbb483-986e-4e3d-b686-bf9ab883fbe4)
