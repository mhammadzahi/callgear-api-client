#app.py
import requests, json, os, csv
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
api_url = 'https://dataapi.callgear.com/v2.0'

def get_calls_report(from_, to_, API_KEY):
    request_data = {
        "jsonrpc": "2.0",
        "id": "number",
        "method": "get.calls_report",
        "params": {
            "access_token": API_KEY,
            "date_from": from_,
            "date_till": to_
        }
    }

    try:
        response = requests.post(api_url, json=request_data)
        print("Status Code:", response.status_code)
        response.raise_for_status()
        data = response.json()
        print("Response JSON received. Processing data...")

        # Check if the expected data is present in the response
        if 'result' in data and 'data' in data['result'] and data['result']['data']:
            call_data = data['result']['data']
            
            # ----------- Data Transformation Start ---------
            # Iterate over each record to add the new URL column
            for record in call_data:
                communication_id = record.get('communication_id')
                call_records_list = record.get('call_records', [])
                
                # Check if there is data to build the links
                if communication_id and call_records_list:
                    links = []
                    for rec_id in call_records_list:
                        # Construct the full URL for each record ID
                        link = f"https://app.callgear.ae/system/media/talk/{communication_id}/{rec_id}/"
                        links.append(link)
                    
                    # Add the generated links to a new field, joined by '**'
                    record['call_records_url'] = '**'.join(links)
                else:
                    # Add an empty string if there are no call records to link to
                    record['call_records_url'] = ''
            # --------------- Data Transformation End ------------------------

        
            # Get headers from the keys of the first *modified* dictionary.
            # This ensures the new 'call_records_url' column is included.
            #headers = call_data[0].keys()
            # Write the transformed data to the CSV file
            # with open('calls_report.csv', 'w', newline='', encoding='utf-8') as csvfile:
            #     writer = csv.DictWriter(csvfile, fieldnames=headers)
            #     writer.writeheader()
            #     writer.writerows(call_data)

            return call_data

        else:
            print("\nNo call data found in the response to generate a CSV file.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")
        return None

    except (KeyError, IndexError) as e:
        print(f"Error processing response data: Could not find call data. Details: {e}")
        return None

    except Exception as e:
        print(e)
        return None

