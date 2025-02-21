import fastapi
from fastapi.middleware.cors import CORSMiddleware

from src.utils import data_utils
from src.data_models import ActuatorType, Event, SensorData, SensorType

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
async def get_event():
    """Get list of events for frontend
    """
    data = data_utils.read_event_data().to_dict(orient='records')
    return {'data': data}


@app.put('/acturator/{actuator_type}')
async def update_acturator(actuator_type: ActuatorType):
    """Control actuator by id

    Args:
        actuator_type (ActuatorType): actuator enum type
    """
    pass


@app.get('/acturator')
async def get_acturator():
    """Get list of actuators for frontend
    """
    pass


@app.get('/sensor')
async def get_sensor():
    """Get list of sensors for frontend
    """
    pass


@app.get('/sensor-data/{sensor_type}')
async def get_sensor_data_by_id(sensor_type: SensorType):
    """Get sensor data by id for frontend

    Args:
        sensor_type (SensorType): sensor enum type
    """
    pass


@app.post('/sensor-data')
async def create_sensor_data(sensor_data: SensorData):
    """Create sensor data from ESP32

    Args:
        sensor_data (SensorData): sensor data model
    """
    data_utils.write_sensor_data(sensor_data, sensor_data.sensor.sensor_type)
    return {'message': 'Sensor Data Successfully Created'}
