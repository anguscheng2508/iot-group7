import fastapi
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from absl import logging

from src.utils import data_utils
from src.utils import sensor_utils
from src.utils import actuator_utils
from src.data_models import ActuatorType, Event, SensorData, SensorType, Sensor, Actuator

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


@app.put('/acturator/{actuator_type}')
async def update_acturator(actuator_type: ActuatorType):
    """Control actuator by id

    Args:
        actuator_type (ActuatorType): actuator enum type
    """
    pass


@app.get('/acturator')
async def get_acturator() -> List[Actuator]:
    """Get list of actuators for frontend
    """
    data = actuator_utils.read_actuator_list()
    data['type'] = data['type'].apply(lambda x: ActuatorType[x.split('.')[1]])
    records = [Actuator(**row) for index, row in data.iterrows()]
    return records


@app.post('/acturator')
async def create_actuator(actuator: Actuator):
    """Create an actuator
    
    Args:
        actuator (Actuator): actuator model
    """
    actuator_utils.write_to_actuator_list(actuator)
    return {'message': f'Actuator {actuator.name} Successfully Created'}


@app.get('/sensor')
async def get_sensor() -> List[Sensor]:
    """Get list of sensors for frontend
    """
    data = sensor_utils.read_sensor_list()
    data['type'] = data['type'].apply(lambda x: SensorType[x.split('.')[1]])
    records = [Sensor(**row) for index, row in data.iterrows()]
    return records


@app.post('/sensor')
async def create_sensor(sensor: Sensor):
    """Create a sensor
    
    Args:
        sensor (Sensor): sensor model
    """
    sensor_utils.write_to_sensor_list(sensor)
    return {'message': f'Sensor {sensor.name} Successfully Created'}


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
