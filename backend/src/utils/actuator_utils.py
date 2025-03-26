import os

import pandas as pd
from src.data_models import Actuator

def read_actuator_list() -> pd.DataFrame:
    """Read csv file from file path. If file does not exist, create an empty file."""
    file_path = f'./data/actuator_list.csv'
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            temp_data = pd.DataFrame(columns=['name', 'type'])
            temp_data.to_csv(file_path, index=False)
            return temp_data
    return pd.read_csv(file_path)


def write_to_actuator_list(actuator: Actuator):
    """Write dataframe to csv file."""
    file_path = f'./data/actuator_list.csv'
    data = read_actuator_list()
    actuator = actuator.model_dump()
    data = pd.concat([data, pd.DataFrame([actuator])], ignore_index=True)
    data.to_csv(file_path, index=False)
    return
