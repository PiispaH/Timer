import json
from pathlib import Path


def write_data(data: dict):
    """Writes the given data into a JSON -file"""
    with open(Path(".data/data.json"), "w") as file:
        json.dump(data, file)
