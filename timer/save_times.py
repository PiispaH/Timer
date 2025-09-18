import json
import os
from utils import DB_PATH


def write_data(data: dict):
    """Writes the given data into a JSON -file"""
    with open(os.path.join(os.path.dirname(DB_PATH), "data.json"), "w") as file:
        json.dump(data, file)
