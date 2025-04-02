import os
from typing import List

import pandas as pd
from absl import logging
from src.data_models import Actuator, ActuatorType


def read_actuator_list() -> pd.DataFrame:
    """Read csv file from file path. If file does not exist, create an empty file."""
    file_path = './data/actuator_list.csv'
    
    if not os.path.exists(file_path):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        data = pd.DataFrame(columns=['name', 'type', 'status'])
    else:
        data = pd.read_csv(file_path)
        # File exists but is empty
        if data.empty:
            data = pd.DataFrame(columns=['name', 'type', 'status'])

    if data.empty:
        default_records = [
            {"name": f"{actuator_type.value}_1", "type": actuator_type.value, "status": "AUTO"}
            for actuator_type in ActuatorType
        ]
        data = pd.DataFrame(default_records)
        data.to_csv(file_path, index=False)

    return data


def write_actuator_list(actuator_data: Actuator):
    """Write dataframe to csv file."""
    file_path = f'./data/actuator_list.csv'
    data = read_actuator_list()
    actuator_data = actuator_data.to_dict()
    data = pd.concat([data, pd.DataFrame([actuator_data])], ignore_index=True)
    data.to_csv(file_path, index=False)
    return


def update_actuator_list(data: List[Actuator]):
    """Update actuator list."""
    file_path = f"./data/actuator_list.csv"
    data.to_csv(file_path, index=False, mode="w")
    return
