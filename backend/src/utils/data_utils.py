# Data IO
import datetime
import os

import pandas as pd
from absl import logging
from src.data_models import Event, SensorData, SensorType, Actuator, ActuatorType


def read_sensor_data(data_enum: SensorType) -> pd.DataFrame:
    """Read csv file from file path. If file does not exist, create an empty file."""
    file_path = f'./data/{data_enum.value}.csv'
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            temp_data = pd.DataFrame(columns=['sensor', 'timestamp', 'value'])
            temp_data.to_csv(file_path, index=False)
            return temp_data
    return pd.read_csv(file_path)


def write_sensor_data(sensor_data: SensorData):
    """Write dataframe to csv file."""
    file_path = f'./data/{sensor_data.sensor.value}.csv'
    data = read_sensor_data(sensor_data.sensor)
    sensor_data.timestamp = datetime.datetime.now()
    sensor_data = sensor_data.model_dump()
    data = pd.concat([data, pd.DataFrame([sensor_data])], ignore_index=True)
    data.to_csv(file_path, index=False)
    return


def read_event_data() -> pd.DataFrame:
    """Read csv file from file path. If file does not exist, create an empty file."""
    file_path = './data/event.csv'
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            temp_data = pd.DataFrame(columns=['device_name', 'timestamp', 'description'])
            temp_data.to_csv(file_path, index=False)
            return temp_data
    return pd.read_csv(file_path)


def write_event_data(event: Event):
    """Write dataframe to csv file."""
    file_path = './data/event.csv'
    data = read_event_data()
    event.timestamp = datetime.datetime.now()
    event_dict = event.model_dump()
    data = pd.concat([data, pd.DataFrame([event_dict])], ignore_index=True)
    data.to_csv(file_path, index=False)
    return


def read_actuator_status() -> pd.DataFrame:
    """Read actuator status from CSV file. If file does not exist, create an empty file."""
    file_path = '/home/ubuntu01/iot-group7/backend/data/actuator.csv'
    if not os.path.exists(file_path):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)  # 修正为使用文件路径的目录
        with open(file_path, 'w') as f:
            temp_data = pd.DataFrame(columns=['name', 'type', 'status', 'timestamp'])
            temp_data.to_csv(file_path, index=False)
            return temp_data
    return pd.read_csv(file_path)
