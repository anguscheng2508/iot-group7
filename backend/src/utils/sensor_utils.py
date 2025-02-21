from src.data_models import SensorData
from src.utils import data_utils

def write_sensor_data(sensor_data: SensorData, file_path: str):
    """Write sensor data to csv file."""
    data = data_utils.read_csv(file_path)
    sensor_data_dict = sensor_data.dict()
    df = df.append(sensor_data_dict, ignore_index=True)
    write_csv(df, file_path)