import datetime
from enum import Enum
from pydantic import BaseModel, ConfigDict


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
    timestamp: datetime.datetime

    model_config = ConfigDict(arbitrary_types_allowed=True)


class Actuator(BaseModel):
    device_id: int
    actuator: ActuatorType


class Sensor(BaseModel):
    device_id: int
    sensor_type: SensorType


class SensorData(BaseModel):
    sensor: Sensor
    timestamp: datetime.datetime
    value: float

    model_config = ConfigDict(arbitrary_types_allowed=True)
