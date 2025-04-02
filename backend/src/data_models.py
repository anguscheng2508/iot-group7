import datetime
from enum import Enum
from typing import Optional, Union, Literal

from pydantic import BaseModel, ConfigDict


class SensorType(Enum):
    TEMPERATURE = 'Temperature'
    HUMIDITY = 'Humidity'
    DISTANCE = 'Distance'
    CO2 = 'CO2'


class ActuatorType(Enum):
    PUMP = 'Pump'
    ALARM = 'Alarm'
    LAMP = 'LAMP'
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
    status: Optional[Literal['ON', 'OFF', 'AUTO']] = 'AUTO'
    
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    def to_dict(self):
        data = self.dict()
        data['type'] = self.type.value
        return data


class DeviceAction(BaseModel):
    device: ActuatorType
    action: Literal['ON', 'OFF', 'AUTO']
