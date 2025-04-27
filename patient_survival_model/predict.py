import sys
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

from typing import Union
import pandas as pd
import numpy as np

from patient_survival_model import __version__ as _version
from patient_survival_model.config.core import config
from patient_survival_model.pipeline import patient_survival_pipe
from patient_survival_model.processing.data_manager import load_pipeline
from patient_survival_model.processing.data_manager import pre_pipeline_preparation
from patient_survival_model.processing.validation import validate_inputs


pipeline_file_name = f"{config.app_config_.pipeline_save_file}{_version}.pkl"
patient_survival_pipe= load_pipeline(file_name=pipeline_file_name)


def make_prediction(*,input_data:Union[pd.DataFrame, dict]) -> dict:
    """Make a prediction using a saved model """
    
    if isinstance(input_data, dict):
        input_df = pd.DataFrame(input_data)
    elif isinstance(input_data, np.ndarray):
        input_df = pd.DataFrame(input_data, columns=config.model_config_.features)
    else:
        input_df = input_data

    validated_data, errors = validate_inputs(input_df=pd.DataFrame(input_data))
    
    #validated_data=validated_data.reindex(columns=['Pclass','Sex','Age','Fare', 'Embarked','FamilySize','Has_cabin','Title'])
    validated_data=validated_data.reindex(columns=config.model_config_.features)
    #print(validated_data)
    results = {"predictions": None, "version": _version, "errors": errors}
    
    predictions = patient_survival_pipe.predict(validated_data)

    results = {"predictions": predictions,"version": _version, "errors": errors}
    print(results.get("predictions")[0])
    if not errors:

        predictions = patient_survival_pipe.predict(validated_data)
        results = {"predictions": predictions,"version": _version, "errors": errors}
        #print(results)

    return results

if __name__ == "__main__":
    age = 60
    anaemia = 0  
    high_blood_pressure = 1  
    creatinine_phosphokinase = 582  
    diabetes = 0  
    ejection_fraction = 38  
    platelets = 265000  
    sex = 1  
    serum_creatinine = 1.9  
    serum_sodium = 130  
    smoking = 0  
    time = 4
    data_in = pd.DataFrame({
        'age': [age],
        'anaemia': [anaemia],
        'high_blood_pressure': [high_blood_pressure],
        'creatinine_phosphokinase': [creatinine_phosphokinase],
        'diabetes': [diabetes],
        'ejection_fraction': [ejection_fraction],
        'platelets': [platelets],
        'sex': [sex],
        'serum_creatinine': [serum_creatinine],
        'serum_sodium': [serum_sodium],
        'smoking': [smoking],
        'time': [time]
    })

    
    make_prediction(input_data=data_in)
