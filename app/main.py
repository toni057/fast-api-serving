import pickle
from typing import Optional, Tuple
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
from sklearn.pipeline import Pipeline


class Iris(BaseModel):
    SepalLength: float
    SepalWidth: float
    PetalLength: float
    PetalWidth: float
    Species: str


app = FastAPI()


class Evaluator:
    def __init__(self, path: Optional[str], pipeline: Optional[Pipeline] = None):
        if path:
            self.pipeline = self.load_pipeline(path)
        elif pipeline:
            self.pipeline = pipeline
        else:
            raise Exception("You need to provide either path or the pipeline.")

    def load_pipeline(self, path: str) -> Pipeline:
        with open(path, "rb") as f:
            m = pickle.load(f)
        return m

    def predict(self, iris: Iris) -> Tuple[str, str]:
        df = pd.DataFrame([iris.dict()])
        predictions = self.pipeline.predict(df.iloc[:, :4].values)[0]
        return df.Species[0], predictions


ev = Evaluator("../models/lr1.pickle")


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.post("/iris")
async def score_model(iris: Iris):
    label, prediction = ev.predict(iris)
    return {
        "species": label,
        "prediction": prediction
    }
