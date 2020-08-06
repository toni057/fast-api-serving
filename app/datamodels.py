from pydantic import BaseModel


class Iris(BaseModel):
    SepalLength: float
    SepalWidth: float
    PetalLength: float
    PetalWidth: float
    Species: str