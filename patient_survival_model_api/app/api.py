# import sys
# from pathlib import Path
# file = Path(__file__).resolve()
# parent, root = file.parent, file.parents[1]
# sys.path.append(str(root))

# import json
# from typing import Any

# import numpy as np
# import pandas as pd
# from fastapi import APIRouter, HTTPException, Body
# from fastapi.encoders import jsonable_encoder
# #from patient_survival_model import __version__ as model_version Remove this 
# from patient_survival_model.predict import make_prediction

# #from app import __version_
# from app import schemas
# from app.config import settings

# api_router = APIRouter()


# @api_router.get("/health", response_model=schemas.Health, status_code=200)
# def health() -> dict:
#     """
#     Root Get
#     """
#     health = schemas.Health(
#         name=settings.PROJECT_NAME, api_version="0.0.1", model_version="0.0.1"
#     )

#     return health.dict()



# example_input = {
#     "inputs": [
#         {
#         "age": 60.0,
#         "anaemia": 0,
#         "high_blood_pressure": 1,
#         "creatinine_phosphokinase": 582,
#         "diabetes": 0,
#         "ejection_fraction": 38,
#         "platelets": 265000.0,
#         "sex": 1,
#         "serum_creatinine": 1.9,
#         "serum_sodium": 130,
#         "smoking": 0,
#         "time": 4,
#         }
#     ]
# }


# @api_router.post("/predict", response_model=schemas.PredictionResults, status_code=200)
# async def predict(input_data: schemas.MultipleDataInputs = Body(..., example=example_input)) -> Any:
#     """
#     Survival predictions with the patient_survival_model
#     """

#     input_df = pd.DataFrame(jsonable_encoder(input_data.inputs))
    
#     results = make_prediction(input_data=input_df.replace({np.nan: None}))

#     if results["errors"] is not None:
#         raise HTTPException(status_code=400, detail=json.loads(results["errors"]))

#     return results

