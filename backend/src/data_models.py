import datetime
from enum import Enum
from typing import Optional, Union

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
    device_name: Union[SensorType, ActuatorType]
    description: str
    timestamp: Optional[datetime.datetime] = None

    model_config = ConfigDict(arbitrary_types_allowed=True)


class SensorData(BaseModel):
    sensor: SensorType
    timestamp: Optional[datetime.datetime] = None
    value: float

    model_config = ConfigDict(arbitrary_types_allowed=True)


class Sensor(BaseModel):
    name: str
    type: SensorType


class Actuator(BaseModel):
    name: str
    type: ActuatorType
    status: Optional[bool] = False
