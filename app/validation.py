import pandas as pd
import pandera as pa

from abc import ABC
from fastapi import HTTPException


class Validator(ABC):
    # def __init__(self, name: str):
    #     self.name = name
    def __init__(self):
        pass

    def validate(self, df: pd.DataFrame):
        pass


class IrisValidator(Validator):
    def __init__(self):
        pass

    def validate(self, df: pd.DataFrame):
        schema = pa.DataFrameSchema({
            "SepalLength": pa.Column(pa.Float),
            "SepalWidth": pa.Column(pa.Float),
            "PetalLength": pa.Column(pa.Float),
            "PetalWidth": pa.Column(pa.Float),
            "Species": pa.Column(pa.String, checks=[
                pa.Check.isin(["setosa", "versicolor", "virginica"])
            ]),
        })

        return schema.validate(df)
