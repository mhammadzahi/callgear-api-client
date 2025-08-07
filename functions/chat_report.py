#app.py
import requests, json, os, csv
from dotenv import load_dotenv


api_url = 'https://dataapi.callgear.com/v2.0'

def get_chat_messages_report(from_, to_, API_KEY):
    request_data = {
        "jsonrpc": "2.0",
        "id": "number",
        "method": "get.chat_messages_report",
        "params": {
            "access_token": API_KEY,
            "date_from": from_,
            "date_till": to_
        }
    }

    try:
        response = requests.post(api_url, json=request_data)
        #print("Status Code:", response.status_code)
        response.raise_for_status()
        data = response.json()
        #print(json.dumps(data, indent=3))
        return data

    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")
        return None

    except (KeyError, IndexError) as e:
        print(f"Error processing response data: Could not find chat messages data. Details: {e}")
        return None

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
