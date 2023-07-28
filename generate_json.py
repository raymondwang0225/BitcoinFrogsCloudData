import json
import random
import os

def generate_json(filename):
    data = {
        "random_number": random.randint(1, 100),
        "message": "Hello, World!"
    }

    # Check if the JSON file already exists
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            try:
                existing_data = json.load(f)
                data['previous_random_number'] = existing_data.get('random_number')
            except json.JSONDecodeError:
                pass

    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    generate_json("BitcoinFrogsCloudData/data.json")
