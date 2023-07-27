import requests
import json
import time
import os
import datetime

url = "https://api.bestinslot.xyz/v3/collection/market_info"

headers = {
    'x-api-key': os.environ.get('MY_BIS_KEY') # 使用環境變數中的 MY_BIS_KEY
}

params = {
    'slug': 'bitcoin-frogs'
}

def get_floor_price(file_path=None):
    # Set default file_path if it is None
    default_file_path = "BitcoinFrogsCloudData/floor_prices.json"

    if file_path is None:
        file_path = default_file_path

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

# Call the function with default file_path if the script is directly executed
if __name__ == "__main__":
    get_floor_price()
