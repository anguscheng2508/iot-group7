# Data IO
import pandas as pd
import os

from src.data_models import Event, SensorData, SensorType


def read_sensor_data(data_enum: SensorType) -> pd.DataFrame:
    """Read csv file from file path. If file does not exist, create an empty file."""
    file_path = f'./data/{data_enum.value}.csv'
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            temp_data = pd.DataFrame(columns=['sensor_type', 'timestamp', 'value'])
            temp_data.to_csv(file_path, index=False)
            return temp_data
    return pd.read_csv(file_path)


def write_sensor_data(sensor_data: SensorData, data_enum: SensorType):
    """Write dataframe to csv file."""
    file_path = f'./data/{data_enum.value}.csv'
    data = read_sensor_data(data_enum)
    sensor_data = sensor_data.model_dump()
    data = pd.concat([data, pd.DataFrame([sensor_data])], ignore_index=True)
    data.to_csv(file_path, index=False)
    return


def read_event_data():
    """Read csv file from file path. If file does not exist, create an empty file."""
    file_path = './data/event.csv'
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            temp_data = pd.DataFrame(columns=['device_id', 'name', 'timestamp', 'description'])
            temp_data.to_csv(file_path, index=False)
            return temp_data
    return pd.read_csv(file_path)


def write_event_data(event: Event):
    """Write dataframe to csv file."""
    file_path = './data/event.csv'
    data = read_event_data()
    event_dict = event.model_dump()
    data = pd.concat([data, pd.DataFrame([event_dict])], ignore_index=True)
    data.to_csv(file_path, index=False)
    return