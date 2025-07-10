import requests, json, os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
api_url = 'https://callapi.callgear.com/v4.0'

def start_call():

    call_request_data = {
        "jsonrpc": "2.0",
        "method": "start.employee_call",
        "id": "req1",
        "params": {
            "access_token": API_KEY,
            "first_call": "employee",
            "virtual_phone_number": "028160531",# dynamic take it from REST APPI
            "direction": "out",
            "contact": "971509267545",
            "employee": {
                "id": 25# dynamic -- take it from REST APPI (by email) https://callgear.github.io/data_api/employee/get_employees/
            }
        }
    }


    try:
        response = requests.post(api_url, json=call_request_data)
        #print("Status Code:", response.status_code)
        print("Response Body:", response.text)
        response.raise_for_status()
        data = response.json()
        print(json.dumps(data, indent=2))

    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")



def get_user_id(email):
    request_data = {
        "email": email
    }

    try:
        response = requests.post(api_url, json=request_data)
        print("[get_user_id] Response Body:", response.text)
        response.raise_for_status()
        data = response.json()
        print(json.dumps(data, indent=2))
        return "ok"

    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")
        return None



if __name__ == "__main__":
    start_call()

