import sys
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier

from patient_survival_model.config.core import config


patient_survival_pipe=Pipeline([
    

     ('model_xg', XGBClassifier(n_estimators=config.model_config_.n_estimators, 
                                         max_depth=config.model_config_.max_depth, 
                                         max_leaves=config.model_config_.max_leaves,
                                         random_state=config.model_config_.random_state))
          
     ])
