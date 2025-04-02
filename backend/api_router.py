from typing import List, Dict

import fastapi
from fastapi import Query, HTTPException, WebSocket, WebSocketDisconnect
from absl import logging
from fastapi.middleware.cors import CORSMiddleware
from src.data_models import (
    Actuator,
    ActuatorType,
    Event,
    Sensor,
    SensorData,
    SensorType,
    DeviceAction,
)
from src.utils import data_utils
from src.utils import actuator_utils

app = fastapi.FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

connected_clients: Dict[str, WebSocket] = {}

@app.websocket("/ws/connect/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await websocket.accept()

    connected_clients[client_id] = websocket
    
    try:
        print(f"Device connected: {client_id}")
        await websocket.send_json({"device": "LAMP", "action": "AUTO"})
        
        # Listening messages from device
        while True:
            data = await websocket.receive_json()
            print(f"Message from device: {data}")
            try:
                device_action = DeviceAction(**data)
                print(f"Received valid data: {device_action.device}")
                
                actuator_list_data = actuator_utils.read_actuator_list()
    
                actuator_index = actuator_list_data.index[actuator_list_data['type'] == device_action.device.value].tolist()
                if not actuator_index:
                    raise HTTPException(status_code=404, detail=f"Actuator of type {device_action.device.value} not found.")

                actuator_list_data.at[actuator_index[0], "status"] = device_action.action

                actuator_utils.update_actuator_list(actuator_list_data)
                
            except ValueError as e:
                await websocket.send_text(f"Invalid data: {e}")
            
    except WebSocketDisconnect:
        print(f"Device disconnected: {client_id}")
        del connected_clients[client_id]


@app.post('/event')
async def create_event(event: Event):
    """Create event from ESP32

    Returns:
        event: Event data model
    """
    data_utils.write_event_data(event)
    return {'message': 'Event Successfully Created'}


@app.get('/event')
async def get_event() -> List[Event]:
    """Get list of events for frontend
    """
    data = data_utils.read_event_data()

    def parse_device_name(name):
        if name.startswith('SensorType.'):
            return SensorType[name.split('.')[1]]
        elif name.startswith('ActuatorType.'):
            return ActuatorType[name.split('.')[1]]
        else:
            raise ValueError(f"Unknown device name: {name}")
    data['device_name'] = data['device_name'].apply(parse_device_name)
    events = [Event(**row) for index, row in data.iterrows()]
    return events


@app.put('/actuator/{actuator_type}')
async def update_actuator(
    actuator_type: str,
    action: str = Query(..., enum=["ON", "OFF", "AUTO"]),
    request_from: str = Query("user_interface", enum=["user_interface", "iot_device"]),
):
    """Control actuator

    Args:
        actuator_type (str): actuator type, e.g. "LAMP"
        action (str): action to be performed, either "ON" or "OFF"
        request_from (str): request source, either "user_interface" or "iot_device"
    """
    
    actuator_type = actuator_type.upper()
    
    if request_from == "user_interface":
        
        if len(connected_clients) != 0:
            websocket = connected_clients["ok"]
            await websocket.send_json({"device": actuator_type, "action": action})
        else:
            raise HTTPException(status_code=404, detail="No WebSocket client connected")
    
    data = actuator_utils.read_actuator_list()
    
    actuator_index = data.index[data['type'] == ActuatorType[actuator_type].value].tolist()
    if not actuator_index:
        raise HTTPException(status_code=404, detail=f"Actuator of type {ActuatorType[actuator_type].value} not found.")

    data.at[actuator_index[0], "status"] = action

    actuator_utils.update_actuator_list(data)

    return {"message": f"Actuator of type {ActuatorType[actuator_type].value} updated successfully.", "new_status": "True" if action == "ON" else "False"}


@app.get('/actuator')
async def get_acturator() -> List[Actuator]:
    """Get list of actuators for frontend
    """
    data = actuator_utils.read_actuator_list()
    actuators = [Actuator(**item) for item in data.to_dict(orient='records')]
    return actuators


@app.get('/sensor')
async def get_sensor() -> List[Sensor]:
    """Get list of sensors for frontend
    """
    sensors = [
        {"name": f"{sensor_type.value}_1", "type": sensor_type}
        for sensor_type in SensorType
    ]
    return sensors


@app.get('/sensor-data/{sensor_type}')
async def get_sensor_data_by_id(sensor_type: SensorType) -> List[SensorData]:
    """Get sensor data by id for frontend

    Args:
        sensor_type (SensorType): sensor enum type
    """
    data = data_utils.read_sensor_data(sensor_type)
    data['sensor'] = data['sensor'].apply(lambda x: SensorType[x.split('.')[1]])
    records = [SensorData(**row) for index, row in data.iterrows()]
    return records


@app.post('/sensor-data')
async def create_sensor_data(sensor_data: SensorData):
    """Create sensor data from ESP32

    Args:
        sensor_data (SensorData): sensor data model
    """
    data_utils.write_sensor_data(sensor_data)
    return {'message': 'Sensor Data Successfully Created'}
