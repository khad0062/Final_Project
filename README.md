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
The IoT sensors are simulated using a Python script that emulates sensors at three Rideau Canal locations: Dow's Lake, Fifth Avenue, and NAC. The script generates data every 10 seconds and sends it to Azure IoT Hub using the Azure IoT Device SDK for Python.


Script Used (sensor-simulation/canalsensor.py):

```python

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
```
Script Details:

1. Library: Uses azure-iot-device for IoT Hub communication.
2. Logic: Loops through locations, generates a JSON payload, serializes it, and sends it to IoT Hub every 10 seconds.
3. Error Handling: Catches exceptions and ensures client shutdown.
4. Dependencies: Requires azure-iot-device (install via pip install azure-iot-device).
5. Execution: Runs indefinitely until stopped, logging sent messages to the console for debugging.
### Data Generation as JSON Format:
```JSON
Sent: {"location": "Dow's Lake", "iceThickness": 20.9, "surfaceTemperature": -3.8, "snowAccumulation": 7.1, "externalTemperature": -6.0, "timestamp": "2025-04-14T15:31:43.069558Z"}
Sent: {"location": "Fifth Avenue", "iceThickness": 21.4, "surfaceTemperature": -2.2, "snowAccumulation": 5.3, "externalTemperature": -7.9, "timestamp": "2025-04-14T15:31:43.514022Z"}
Sent: {"location": "NAC", "iceThickness": 23.9, "surfaceTemperature": -4.8, "snowAccumulation": 3.0, "externalTemperature": -1.2, "timestamp": "2025-04-14T15:31:43.641111Z"}
```
The script authenticates with IoT Hub using a device-specific connection string.
Messages are sent asynchronously, with the SDK handling retries and connectivity issues
   - **Azure IoT Hub Configuration**:
     Azure IoT Hub is configured to ingest sensor data from the simulated devices and route it to Azure Stream Analytics for processing.

## Configuration Steps:

### Create IoT Hub:
1. In Azure Portal, navigate to "Create a resource" and select "IoT Hub."
2. Choose a subscription, resource group, and region.
3. Select the Free tier (F1) for testing or an appropriate pricing tier.
4. Name the IoT Hub (e.g., RideauCanalIoTHub).
### Register Device:
1. In the IoT Hub, go to "Devices" under "Device management."
2. Add a new device (e.g., CanalSensor).
3. Copy the primary connection string for the device (format: HostName=<hub-name>.azure-devices.net;DeviceId=CanalSensor;SharedAccessKey=<key>).
4. Use this string in the simulation script.
### Configure Endpoints:
IoT Hub has a built-in endpoint (messages/events) for device-to-cloud messages.
No custom endpoints are needed for this setup, as data is routed to Stream Analytics.
   - **Azure Stream Analytics Job**:
     The Azure Stream Analytics job processes incoming sensor data from IoT Hub in real time, aggregates it over 5-minute windows, and outputs the results to Azure Blob Storage.

Job Configuration:

### Create Job:
1. In Azure Portal, create a new Stream Analytics job (e.g., CanalAnalytics).
2. Assign it to a resource group and select a region.
3. Set streaming units (e.g., 1 for small-scale processing).
4. Define Input:
5. Add an input:
6. Type: Stream.
7. Source: IoT Hub.
8. Alias: SensorInput.
IoT Hub: Select the configured IoT Hub (RideauCanalIoTHub).
Consumer Group: Use the default ($Default) or create a new one.
Authentication: Use managed identity or IoT Hub access keys.
Define Output:
Add an output:
Type: Blob Storage/Data Lake Storage Gen2.
Alias: BlobOutput.
Storage Account: Select the configured storage account (e.g., canalstorage).
Container: Use canal-data.
Path Pattern: output/{date}/{location} (e.g., output/2024-11-23/DowsLake).
Date Format: YYYY-MM-DD.
Authentication: Use managed identity or storage account key.
Query Logic:
The query aggregates data per location over a 5-minute tumbling window.
Calculates:
Average ice thickness (avgIceThickness).
Maximum snow accumulation (maxSnowAccumulation).
Includes the window end time for reference.
Sample Query:

sql

Copy
SELECT
    location,
    AVG(iceThickness) AS avgIceThickness,
    MAX(snowAccumulation) AS maxSnowAccumulation,
    System.Timestamp() AS windowEndTime
INTO BlobOutput
FROM SensorInput
GROUP BY location, TumblingWindow(minute, 5)
Query Explanation:

Input: SensorInput reads JSON payloads from IoT Hub.
Grouping: Groups data by location and 5-minute windows using TumblingWindow.
Aggregations:
AVG(iceThickness) computes the mean ice thickness.
MAX(snowAccumulation) finds the highest snow accumulation.
Output: Writes results to BlobOutput as JSON.
Timestamp: Uses System.Timestamp() to mark the end of each window.
Output Destination:

Data is sent to Azure Blob Storage in JSON format, organized by date and location
   - **Azure Blob Storage**:
     - Explain how the processed data is organized in Blob Storage (e.g., folder structure, file naming convention).
     - Specify the formats of stored data (JSON/CSV).
![image](https://github.com/user-attachments/assets/6fcbb483-986e-4e3d-b686-bf9ab883fbe4)
