#app.py
import requests, json, os, csv
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
api_url = 'https://dataapi.callgear.com/v2.0'

def get_calls_report(from_date, to_date):
    request_data = {
        "jsonrpc": "2.0",
        "id": "number",
        "method": "get.calls_report",
        "params": {
            "access_token": API_KEY,
            "date_from": from_date,
            "date_till": to_date
        }
    }

    try:
        response = requests.post(api_url, json=request_data)
        #print("Status Code:", response.status_code)
        response.raise_for_status()  # Raises an exception for bad status codes
        data = response.json()
        print(json.dumps(data, indent=2))

        # Check if the expected data is present in the response
        if 'result' in data and 'data' in data['result'] and data['result']['data']:
            call_data = data['result']['data']
            
            csv_file_name = f'Calls_Report_{from_date}__To__{to_date}.csv'
            
            # Get the headers from the keys of the first dictionary in the list
            headers = call_data[0].keys()
            
            # Write data to the CSV file
            with open(csv_file_name, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                writer.writeheader()
                writer.writerows(call_data)
            
            print(f"\nSuccessfully generated CSV file: {csv_file_name}")

        else:
            print("\nNo call data found in the response to generate a CSV file.")


    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")

    except (KeyError, IndexError) as e:
        print(f"Error processing response data: Could not find call data. Details: {e}")
        
    except Exception as e:
        print(f"An unexpected error occurred: {e}")



if __name__ == "__main__":
    get_calls_report("2025-07-01 00:00:00", "2025-07-29 05:00:00")
