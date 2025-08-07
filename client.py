import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = "http://localhost:8004"



yesterday = datetime.now() - timedelta(days=1)
start_date = yesterday.strftime("%Y-%m-%d 00:00:00")
end_date = yesterday.strftime("%Y-%m-%d 23:59:59")

headers = {
    "X-API-KEY": API_KEY,
    "Content-Type": "application/json"
}

payload = {
    "start_date": start_date,
    "end_date": end_date
}


def run_reports():
    
    calls_response = requests.post(f"{BASE_URL}/save-calls-report", json=payload, headers=headers)
    print("Calls report response:", calls_response.status_code, calls_response.json())

    #chat_response = requests.post(f"{BASE_URL}/save-chat-messages-report", json=payload, headers=headers)
    #print("Chat messages report response:", chat_response.status_code, chat_response.json())

if __name__ == "__main__":
    run_reports()
