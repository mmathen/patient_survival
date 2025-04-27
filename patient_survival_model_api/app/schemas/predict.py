from typing import Any, List, Optional

from pydantic import BaseModel


class PredictionResults(BaseModel):
    errors: Optional[Any]
    version: str
    #predictions: Optional[List[int]]
    predictions: Optional[int]

class DataInputSchema(BaseModel):
    age: Optional[float]
    anaemia: Optional[int]
    high_blood_pressure: Optional[int]
    creatinine_phosphokinase: Optional[int]
    diabetes: Optional[int]
    ejection_fraction: Optional[int]
    platelets: Optional[float]
    sex: Optional[int]
    serum_creatinine: Optional[float]
    serum_sodium: Optional[int]
    smoking: Optional[int]
    time: Optional[int]


class MultipleDataInputs(BaseModel):
    inputs: List[DataInputSchema]

