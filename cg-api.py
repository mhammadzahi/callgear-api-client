import os
from datetime import datetime
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Security, status
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from functions.calls_report import get_calls_report
from functions.chat_report import get_chat_messages_report
from functions.database import Database



load_dotenv()

API_KEY = os.getenv("API_KEY")
CG_API_KEY = os.getenv("CG_API_KEY")
DB_URL = os.getenv("DB_URL")

class DateRange(BaseModel):
    start_date: str
    end_date: str


app = FastAPI()
db = Database(DB_URL)

api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=True)

def get_api_key(api_key: str = Security(api_key_header)):
    if api_key == API_KEY:
        return api_key

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing API Key")



@app.post("/get-calls-report")
def calls_report(date_range: DateRange, api_key: str = Depends(get_api_key)):

    if not (call_report := get_calls_report(date_range.start_date, date_range.end_date, CG_API_KEY)):
        return {"success": False}, 400

    if not db.insert_call_reports(call_report):
        return {"success": False}, 500

    return {"success": True}, 200


# @app.post("/get-chat-messages-report")
# def chat_messages_report(date_range: DateRange, api_key: str = Depends(get_api_key)):
#     chat_report = get_chat_messages_report(date_range.start_date, date_range.end_date, CG_API_KEY)
#     db.sync_chat_messages_report(chat_report)
#     return {"success": True}


@app.get("/")
def read_root():
    return {"message": "API, V1.3.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("cg-api:app", host="0.0.0.0", port=8004, reload=True)# dev
    #uvicorn.run(app, host="0.0.0.0", port=8004)# prod
