from typing import Optional
from fastapi import FastAPI, HTTPException

from app.scoring import IrisScorer
from app.datamodels import Iris

app = FastAPI()
ev = IrisScorer("./models/lr1.pickle")


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.post("/iris")
async def score_model(iris: Iris):
    ret = ev.score(iris)

    if isinstance(ret, HTTPException):
        raise ret
    else:
        label, prediction = ret
        return {
            "species": label,
            "prediction": prediction
        }
