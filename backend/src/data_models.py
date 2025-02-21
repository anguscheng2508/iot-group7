import datetime
from enum import Enum
from pydantic import BaseModel


class SensorType(Enum):
    TEMPERATURE = 'Temperature'
    HUMIDITY = 'Humidity'
    DISTANCE = 'Distance'
    CO2 = 'CO2'


class ActuatorType(Enum):
    PUMP = 'Pump'
    ALARM = 'Alarm'
    LIGHT = 'Light'
    WINDOW = 'Window'
    FAN = 'Fan'


class Event(BaseModel):
    """Event data model
    """
    device_id: int
    name: str
    description: str
    created_at: str


class Actuator(BaseModel):
    device_id: int
    actuator: ActuatorType


class Sensor(BaseModel):
    device_id: int
    sensor_type: SensorType


class SensorData(BaseModel):
    sensor: Sensor
    timestamp: datetime
    value: float
