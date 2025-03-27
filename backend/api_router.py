from typing import List

import fastapi
from absl import logging
from fastapi.middleware.cors import CORSMiddleware
from src.data_models import (
    Actuator,
    ActuatorType,
    Event,
    Sensor,
    SensorData,
    SensorType,
)
from src.utils import data_utils

app = fastapi.FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex='http.*',
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


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




@app.get('/actuator')
async def get_actuator() -> List[Actuator]:
    """Get list of actuators for frontend"""
    data = data_utils.read_actuator_status()

    if data.empty:
        return [
            Actuator(name=f"{actuator_type.value}_1", type=actuator_type, status=False)
            for actuator_type in ActuatorType
        ]
    
    actuators = []
    for index, row in data.iterrows():
        type_value = row['type']
        actuator_type = next((at for at in ActuatorType if at.value == type_value), None)
        if actuator_type is None:
            continue 
        actuators.append(
            Actuator(
                name=row['name'],
                type=actuator_type,
                status=bool(row['status'])
            )
        )
    return actuators
# @app.get('/actuator')
# async def get_acturator() -> List[Actuator]:
#     """Get list of actuators for frontend
#     """
#     actuators = [
#         {"name": f"{actuator_type.value}_1", "type": actuator_type}
#         for actuator_type in ActuatorType
#     ]
#     return actuators


# @app.put('/actuator/{actuator_type}')
# async def update_actuator(actuator: Actuator):
#     """Control actuator by id

#     Args:
#         actuator_type (ActuatorType): actuator enum type
#     """
#     pass

@app.put('/actuator/{actuator_type}')
async def update_actuator(actuator_type: ActuatorType):
    """Control actuator by type - toggle the status of all actuators of the given type"""
    current_data = data_utils.read_actuator_status()
    
    current_actuators = []
    if not current_data.empty:
        for _, row in current_data.iterrows():
            type_value = row['type']
            actuator_type_found = next((at for at in ActuatorType if at.value == type_value), None)
            if actuator_type_found is None:
                continue
            current_actuators.append(
                Actuator(
                    name=row['name'],
                    type=actuator_type_found,
                    status=bool(row['status'])
                )
            )
    else:
        raise fastapi.HTTPException(
            status_code=404,
            detail=f"No actuators found in the system"
        )
    
    updated = False
    new_status = None  
    for actuator in current_actuators:
        if actuator.type == actuator_type:
            actuator.status = not actuator.status  
            new_status = actuator.status 
            updated = True
    
    if not updated:
        raise fastapi.HTTPException(
            status_code=404,
            detail=f"No actuators of type {actuator_type.value} found"
        )

    data_utils.write_actuator_status(current_actuators)
    
    status_str = "on" if new_status else "off"
    description = f"Toggled status of {actuator_type.value} actuators to {status_str}"
    
    event = Event(
        device_name=actuator_type,
        description=description
    )
    data_utils.write_event_data(event)
    
    return {"message": f"Status of actuators of type {actuator_type.value} toggled to {status_str}"}




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
