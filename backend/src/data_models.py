import datetime
from enum import Enum
from pydantic import BaseModel, ConfigDict
from typing import Optional, Union


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
