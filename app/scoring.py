import pickle
import pandas as pd
import pandera as pa

from typing import Optional, Tuple
from sklearn.pipeline import Pipeline
from fastapi import HTTPException
from abc import ABC

from app.datamodels import Iris
from app.validation import Validator, IrisValidator


class Scorer(ABC):
    def __init__(self, pipeline: Pipeline):
        self.pipeline = pipeline

    def score(self):
        pass

    def load_pipeline(self, path: str) -> Pipeline:
        with open(path, "rb") as f:
            m = pickle.load(f)
        return m


class IrisScorer(Scorer):
    def __init__(self, path: Optional[str], pipeline: Optional[Pipeline] = None, validator: Optional[Validator] = None):
        if path:
            pipeline = self.load_pipeline(path)
        elif not pipeline:
            raise Exception("You need to provide either path or the pipeline.")

        super().__init__(pipeline)

        if not validator:
            self.validator = IrisValidator()

    def score(self, iris: Iris) -> Tuple[str, str]:
        df = pd.DataFrame([iris.dict()])

        if self.validator:
            try:
                df = self.validator.validate(df)
                predictions = self.pipeline.predict(df.iloc[:, :4].values)[0]
                return df.Species[0], predictions

            except pa.errors.SchemaError as e:
                return HTTPException(status_code=403, detail=str(e.check))
