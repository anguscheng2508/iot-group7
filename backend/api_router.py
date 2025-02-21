import fastapi
from fastapi.middleware.cors import CORSMiddleware

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
    return {'message': 'Event Successfully Created'}


@app.get('/event')
async def get_event():
    """Get list of events for frontend
    """
    pass


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
    pass