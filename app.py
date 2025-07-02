import requests
import json

api_url = 'https://dataapi.callgear.com/v2.0'

request_data = {
    "jsonrpc": "2.0",
    "id": "number",
    "method": "get.calls_report",
    "params": {
        "access_token": "",
        "date_from": "2025-06-25 00:00:00",
        "date_till": "2025-07-01 23:59:59"
    }
}

try:
    response = requests.post(api_url, json=request_data)
    print("Status Code:", response.status_code)
    print("Response Body:", response.text)
    response.raise_for_status()
    data = response.json()
    print(json.dumps(data, indent=2))

except requests.exceptions.RequestException as e:
    print(f"Error during request: {e}")
