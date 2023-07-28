import requests
import json
import time
import os
import datetime

url = "https://api.bestinslot.xyz/v3/collection/market_info"

headers = {
    'x-api-key': os.environ.get('MY_BIS_KEY') # 使用环境变量中的 MY_BIS_KEY
}

params = {
    'slug': 'bitcoin-frogs'
}

def get_floor_price():
    # Set file_path to 'floor_prices.json' in the repository's root directory
    file_path = os.path.join(os.getenv('GITHUB_WORKSPACE'), "floor_prices.json")

    # Set default values if folder_path and file_path are None
    
    current_data = []

    
    response = requests.get(url, headers=headers, params=params)
    json_data = response.json()

    if json_data['data']:
        min_price = round(json_data['data']['floor_price']/100000000, 4)

    try:
        with open(file_path, "r") as file:
            current_data = json.load(file)
    except FileNotFoundError:
        current_data = []

    current_time = int(datetime.datetime.utcnow().timestamp())
    current_timeformat = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    new_entry = {"time": current_time, "value": min_price}
    current_data.insert(0, new_entry)

    with open(file_path, "w") as file:
        json.dump(current_data, file, indent=None)

    # Run git pull and resolve conflicts if needed
    try:
        subprocess.run(["git", "pull", "origin", "main"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        # If there is a conflict, resolve it and commit the changes
        if "CONFLICT" in e.stderr.decode("utf-8"):
            subprocess.run(["git", "add", file_path])
            subprocess.run(["git", "commit", "-m", "Resolve conflicts"])
            subprocess.run(["git", "push", "origin", "HEAD:main"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

if __name__ == "__main__":
    get_floor_price()
