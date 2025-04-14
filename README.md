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
     - Describe how the simulated IoT sensors generate and send data to Azure IoT Hub.
     - Include the structure of the JSON payload and any scripts or applications used.
   - **Azure IoT Hub Configuration**:
     - Explain the configuration steps for setting up the IoT Hub, including endpoints and message routing.
   - **Azure Stream Analytics Job**:
     - Describe the job configuration, including input sources, query logic, and output destinations.
     - Provide sample queries used for data processing.
   - **Azure Blob Storage**:
     - Explain how the processed data is organized in Blob Storage (e.g., folder structure, file naming convention).
     - Specify the formats of stored data (JSON/CSV).
