# Final Project Assignment: Real-time Monitoring System for Rideau Canal Skateway


## 1. Scenario Description ##
This project implements a real-time monitoring system for the Rideau Canal Skateway using simulated IoT sensors, Azure IoT Hub, Azure Stream Analytics, and Azure Blob Storage. The system simulates sensor data (ice thickness, surface temperature, snow accumulation, external temperature) from three locations, processes it in real time, and stores aggregated outputs in Blob Storage.

## 2. System Architecture:  
   ![Overall Architecutre Diagram](https://github.com/user-attachments/assets/1e11a6a1-c5dc-4f7d-931f-950313fa6f71) 

                            Fig: Overall Architecture Diagram

   ![Data Flow](https://github.com/user-attachments/assets/e05e9ac1-d06a-457f-acf6-e16547359309)

                            Fig: Data Flow 

## 3. Implementation Details ##
   ### 3.1 IoT Sensor Simulation ###
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
6. The script authenticates with IoT Hub using a device-specific connection string.

### Data Generation as JSON Format:
```
Sent: {"location": "Dow's Lake", "iceThickness": 20.9, "surfaceTemperature": -3.8, "snowAccumulation": 7.1, "externalTemperature": -6.0, "timestamp": "2025-04-14T15:31:43.069558Z"}
Sent: {"location": "Fifth Avenue", "iceThickness": 21.4, "surfaceTemperature": -2.2, "snowAccumulation": 5.3, "externalTemperature": -7.9, "timestamp": "2025-04-14T15:31:43.514022Z"}
Sent: {"location": "NAC", "iceThickness": 23.9, "surfaceTemperature": -4.8, "snowAccumulation": 3.0, "externalTemperature": -1.2, "timestamp": "2025-04-14T15:31:43.641111Z"}
```


### 3.2 Azure IoT Hub Configuration
Azure IoT Hub is configured to ingest sensor data from the simulated devices and route it to Azure Stream Analytics for processing.

### Configuration Steps:
#### Create IoT Hub:
1. In Azure Portal, navigate to "Create a resource" and select "IoT hub"
2. Choose a subscription`Azure for students`, resource group `IoT`, and region `Canada Central`.
3. Select the Free tier (F1) for testing or an appropriate pricing tier.
4. Name the IoT Hub:`rideaucanalIOT`.
#### Register Device:
- In the IoT Hub, go to "Devices" under "Device management."
- Add a new device and add new devic id (i.e.`canalsensor`).
- Copy the primary connection string for the device (format: HostName=<hub-name>.azure-devices.net;DeviceId=CanalSensor;SharedAccessKey=<key>).
- Use this string in the simulation script.
 #### Install Required Libraries
Install the azure-iot-device library to simulate sensor data. Run the following command:
``` pip install azure-iot-device ```
#### Run the Python Script to Simulate Sensor Data
Use the following Python script to simulate telemetry data and send it to the IoT Hub. Replace the CONNECTION_STRING with the device connection string.
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

Execute the script to start sending telemetry data to IoT Hub with the python command : python canalsensor.py .

### 3.3 Azure Blob Storage
#### Create Storage Account
- In Azure Portal, create: `rideauiotstorageaccount`.
- Choose resource group i.e. IoT, region: canada central.
- Use standard performance, LRS.

#### Create Container
- Name: `iotoutput`.
- Access: Private.

### 3.4 Azure Stream Analytics Job
The Stream Analytics job processes data from Azure IoT Hub, aggregates it over 5-minute windows, and outputs the results to Azure Blob Storage.

### Configuration Steps

#### Create Job
  - In the Azure Portal, create a Stream Analytics job named `processiot`.
  - Assign the job to a resource group (IoT) and select a region: canada central.
  - Hosting environment to Cloud.
  - Set the streaming units to 1.

#### Define Input
- **Type**: Stream
- **Source**: IoT Hub (named `rideaucanalIOT`)
- **Alias**: `IoTsensorinput`
- **Consumer Group**: `$Default`
- **Authentication**: access keys

#### Define Output
- **Type**: Blob Storage
- **Alias**: `iotsensoroutput`
- **Storage Account**: `rideauiotstorageaccount`
- **Container**: `iotoutput`
- **Authentication**:Storage account key

#### Sample Query
```sql
SELECT
    location,
    AVG(iceThickness) AS avgIceThickness,
    MAX(snowAccumulation) AS maxSnowAccumulation,
    System.Timestamp() AS windowEndTime
INTO iotsensoroutput
FROM IoTsensorinput
GROUP BY location, TumblingWindow(minute, 5)
```
The job aggregates data per location over 5-minute tumbling windows and computes:
- The average ice thickness (`avgIceThickness`)
- The maximum snow accumulation (`maxSnowAccumulation`)

#### Save and Start the Job
Save the query and click Start on the Stream Analytics job.

### 3.5 Verify the Output
1. Monitor the Stream Analytics Job
Navigate to the Monitoring tab of the job to view metrics and ensure data is being processed.

2. Check Blob Storage
   - Go to your Azure Storage Account.
   - Navigate to the container specified in the output i.e.`iotsensoroutput` .
   - Verify that processed data is being stored in JSON format.

#### Result
**Path**: `0_0a7fe6f699714f67a8b86dff6161f6e3_1.json`
```json
"location":"Dow's Lake","avgIceThickness":24.879310344827587,"maxSnowAccumulation":9.9,"windowEndTime":"2025-04-14T15:45:00.0000000Z"}
{"location":"NAC","avgIceThickness":25.268965517241387,"maxSnowAccumulation":9.8,"windowEndTime":"2025-04-14T15:45:00.0000000Z"}
{"location":"Fifth Avenue","avgIceThickness":25.76206896551724,"maxSnowAccumulation":9.4,"windowEndTime":"2025-04-14T15:45:00.0000000Z"}
```
