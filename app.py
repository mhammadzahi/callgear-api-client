import os
from datetime import datetime

import uvicorn
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Security, status
from fastapi.security import APIKeyHeader
from pydantic import BaseModel


load_dotenv()

API_KEY = os.getenv("API_KEY")
CG_API_KEY = os.getenv("CG_API_KEY")

class DateRange(BaseModel):
    start_date: datetime
    end_date: datetime


app = FastAPI()

api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=True)

def get_api_key(api_key: str = Security(api_key_header)):
    if api_key == API_KEY:
        return api_key

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key"
    )


@app.get("/")
def read_root():
    return {"message": "API for Date Validation, V1.3.0"}

@app.post("/validate-dates/")
def validate_date_range(date_range: DateRange, api_key: str = Depends(get_api_key)):
    return {
        "message": "API key is valid. Dates received successfully.",
        "received_start_date": date_range.start_date,
        "received_end_date": date_range.end_date,
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
