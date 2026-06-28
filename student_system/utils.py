import json


def load_students(filepath):
    with open(filepath, "r") as file:
        return json.load(file)
