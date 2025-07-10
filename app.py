import requests, json, os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
api_url = 'https://dataapi.callgear.com/v2.0'

def start_call():

    call_request_data = {
        "jsonrpc": "2.0",
        "method": "start.employee_call",
        "id": "req1",
        "params": {
            "access_token": API_KEY,
            "first_call": "employee",
            "virtual_phone_number": "74993720692",
            "direction": "out",
            "contact": "79260000000",
            "employee": {
            "id": 25,
            "phone_number": "79260000001"
            },
            "contact_message": {
            "type": "tts",
            "value": "Hello"
            },
            "employee_message": {
            "type": "media",
            "value": "2561"
            }
        }
    }


    try:
        response = requests.post(api_url, json=call_request_data)
        print("Status Code:", response.status_code)
        print("Response Body:", response.text)
        response.raise_for_status()
        data = response.json()
        print(json.dumps(data, indent=2))

    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")


if __name__ == "__main__":
    get_calls_report()
