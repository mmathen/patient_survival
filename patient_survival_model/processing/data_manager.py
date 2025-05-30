import sys
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

import re
import joblib
import pandas as pd
import typing as t
from sklearn.pipeline import Pipeline

from patient_survival_model import __version__ as _version
from patient_survival_model.config.core import DATASET_DIR, TRAINED_MODEL_DIR, config



def get_outlier_columns(data: pd.DataFrame) -> list:
    outlier_colms = ['creatinine_phosphokinase', 'ejection_fraction', 'platelets', 'serum_creatinine', 'serum_sodium']
    return outlier_colms

def handle_outliers ( data:pd.DataFrame, colms: list) -> pd.DataFrame:
    data_copy = data.copy() # Create a copy of the DataFrame to avoid modifying the original
    for col in colms:
        '''Change the values of outlier to upper and lower whisker values '''
        q1 = data_copy.describe()[col].loc["25%"]
        q3 = data_copy.describe()[col].loc["75%"]
        iqr = q3 - q1
        lower_bound = q1 - (1.5 * iqr)
        upper_bound = q3 + (1.5 * iqr)
        for i in range(len(data_copy)):
            if data_copy.loc[i,col] > upper_bound:
                data_copy.loc[i,col]= upper_bound
            if data_copy.loc[i,col] < lower_bound:
                data_copy.loc[i,col]= lower_bound
    return data_copy
        

def pre_pipeline_preparation(*, data_frame: pd.DataFrame) -> pd.DataFrame:

    cleaned_data = handle_outliers(data=data_frame, colms=get_outlier_columns(data=data_frame))

    return cleaned_data



def load_raw_dataset(*, file_name: str) -> pd.DataFrame:
    dataframe = pd.read_csv(Path(f"{DATASET_DIR}/{file_name}"))
    return dataframe

def load_dataset(*, file_name: str) -> pd.DataFrame:
    dataframe = pd.read_csv(Path(f"{DATASET_DIR}/{file_name}"))
    transformed = pre_pipeline_preparation(data_frame=dataframe)
    return transformed


def save_pipeline(*, pipeline_to_persist: Pipeline) -> None:
    """Persist the pipeline.
    Saves the versioned model, and overwrites any previous
    saved models. This ensures that when the package is
    published, there is only one trained model that can be
    called, and we know exactly how it was built.
    """

    # Prepare versioned save file name
    save_file_name = f"{config.app_config_.pipeline_save_file}{_version}.pkl"
    save_path = TRAINED_MODEL_DIR / save_file_name

    remove_old_pipelines(files_to_keep=[save_file_name])
    joblib.dump(pipeline_to_persist, save_path)
    print("Model/pipeline trained successfully!")


def load_pipeline(*, file_name: str) -> Pipeline:
    """Load a persisted pipeline."""

    file_path = TRAINED_MODEL_DIR / file_name
    trained_model = joblib.load(filename=file_path)
    return trained_model


def remove_old_pipelines(*, files_to_keep: t.List[str]) -> None:
    """
    Remove old model pipelines.
    This is to ensure there is a simple one-to-one
    mapping between the package version and the model
    version to be imported and used by other applications.
    """
    do_not_delete = files_to_keep + ["__init__.py", ".gitignore"]
    for model_file in TRAINED_MODEL_DIR.iterdir():
        if model_file.name not in do_not_delete:
            model_file.unlink()

