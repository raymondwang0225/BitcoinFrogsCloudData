import requests
import json
import time
import os
import datetime

bis_key = os.environ.get('MY_BIS_KEY')

url = "https://api.bestinslot.xyz/v3/collection/market_info"

headers = {
    'x-api-key': bis_key
}

params = {
    'slug': 'bitcoin-frogs'
}

def get_floor_price(folder_path=None, file_path=None):
    # Set default values if folder_path and file_path are None
    default_folder_path = "Bitcoin_Frogs_Data"
    default_file_path = os.path.join(default_folder_path, "floor_prices.json")
    current_data = []

    if folder_path is None:
        folder_path = default_folder_path

    if file_path is None:
        file_path = default_file_path

    # Create the folder if it does not exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    response = requests.get(url, headers=headers, params=params)
    json_data = response.json()

    if json_data['data']:
        min_price = round(json_data['data']['floor_price']/100000000,4)
       

    # Create the folder if it does not exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    try:
        with open(file_path, "r") as file:
            current_data = json.load(file)
    except FileNotFoundError:
        current_data = []

    #current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    current_time = int(datetime.datetime.utcnow().timestamp())
    current_timeformat = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")


    new_entry = {"time": current_time, "value": min_price}

    current_data.insert(0, new_entry)

    with open(file_path, "w") as file:
        json.dump(current_data, file, indent=None)




get_floor_price()
