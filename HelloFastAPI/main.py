# uvicorn 起動
# $ uvicorn main:app --reload

from fastapi import FastAPI
from typing import Optional, List
from pydantic import BaseModel, Field

app = FastAPI()

@app.get("/")
async def index():
    return  {"message": "Hello World"}



@app.get("/countries/")
async def country(country_name: Optional[str]=None, country_no: Optional[int]=None):
    return  {
        "country_name": country_name,
        "country_no": country_no
            }


class ShopInfo(BaseModel):
    name: str
    location: str


class Item(BaseModel):
    name: str = Field(default="dffff", min_length=4, max_length=12)
    descriptiion: Optional[str] = None
    price: int
    tax: Optional[float] = None

class Data(BaseModel):
    shop_info: Optional[ShopInfo] = None
    items: List[Item]


@app.post("/shop_items/")
async def index(data: Data):
    return {"data": data}
