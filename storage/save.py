
import json
import os

def save_json(data, filename):
    os.makedirs("data/bills_json", exist_ok=True)
    path = os.path.join("data/bills_json", filename)
    with open(path, "w") as f:
        json.dump(data, f, indent=4)