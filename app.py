import os
import uuid
from contextlib import asynccontextmanager

import psycopg2
import uvicorn
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Security, status
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, Field

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
CG_API_KEY = os.getenv("CG_API_KEY")
API_KEY = os.getenv("API_KEY")

class Item(BaseModel):
    name: str
    description: str | None = None


app = FastAPI()

api_key_header = APIKeyHeader(name="X-API-KEY")

def get_api_key(api_key: str = Security(api_key_header)) -> str:
    if api_key == API_KEY:
        return api_key
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing API Key")



@app.post("/items/", response_model=ItemInDB)
async def create_item(item: Item, api_key: str = Depends(get_api_key)):
    """
    Create a new item in the database.

    This endpoint requires a valid API key in the `X-API-KEY` header.
    """
    try:
        with app.state.db_conn.cursor() as cur:
            item_id = uuid.uuid4()
            cur.execute(
                "INSERT INTO items (id, name, description) VALUES (%s, %s, %s)",
                (str(item_id), item.name, item.description),
            )
            app.state.db_conn.commit()
            return {"id": item_id, "name": item.name, "description": item.description}
    except psycopg2.Error as e:
        app.state.db_conn.rollback()
        raise HTTPException(status_code=500, detail="Database error") from e



@app.get("/")
def read_root():
    return {"message": "Hello, CG API, V1.1.2"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("gps-api:app", host="0.0.0.0", port=8001, reload=True)# dev
    #uvicorn.run(app, host="0.0.0.0", port=8001)# prod
