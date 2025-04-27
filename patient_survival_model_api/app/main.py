import sys
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))
#print(sys.path)
from typing import Any

from fastapi import APIRouter, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi.responses import HTMLResponse
import gradio as gr

from app.api import api_router
from app.config import settings
#from patient_survival_model import make_prediction
from patient_survival_model import __version__ as model_version
from patient_survival_model.predict import make_prediction

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

root_router = APIRouter()


@root_router.get("/")
def index(request: Request) -> Any:
    """Basic HTML response."""
    body = (
        "<html>"
        "<body style='padding: 10px;'>"
        "<h1>Welcome to the API</h1>"
        "<div>"
        "Check the docs: <a href='/docs'>here</a>"
        "</div>"
        "</body>"
        "</html>"
    )

    return HTMLResponse(content=body)

title = "Patient Survival Prediction"
description = "Predict survival of patient with heart failure, given their clinical record"



# fastapi_app = FastAPI()

def gradio_predict_death_event(age: float, anaemia: int, creatinine_phosphokinase: int, diabetes: int, ejection_fraction: int, high_blood_pressure: int, platelets: float, sex: int, serum_creatinine: float, serum_sodium: int, smoking: int, time: int):
    """Calls the packaged prediction function directly."""
    input_data = pd.DataFrame({
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
    prediction_result = make_prediction(input_data=input_data)
    if prediction_result and 'predictions' in prediction_result and len(prediction_result['predictions']) > 0:
        return f"Prediction: {prediction_result['predictions'][0]}"
    else:
        return "Error in prediction."

gradio_app = gr.Interface(
    fn=gradio_predict_death_event,
    inputs=[
        gr.Slider(minimum=40, maximum=95, step=1, label="Age"),
        gr.Radio([0, 1], label="Anaemia (0 = No, 1 = Yes)"),
        gr.Slider(minimum=23, maximum=7861, step=1, label="Creatinine Phosphokinase (mcg/L)"),
        gr.Radio([0, 1], label="Diabetes (0 = No, 1 = Yes)"),
        gr.Slider(minimum=14, maximum=80, step=1, label="Ejection Fraction (%)"),
        gr.Radio([0, 1], label="High Blood Pressure (0 = No, 1 = Yes)"),
        gr.Slider(minimum=25000, maximum=850000, step=1000, label="Platelets (kiloplatelets/mL)"),
        gr.Slider(minimum=0.5, maximum=9.4, step=0.1, label="Serum Creatinine (mg/dL)"),
        gr.Slider(minimum=113, maximum=148, step=1, label="Serum Sodium (mEq/L)"),
        gr.Radio([0, 1], label="Sex (0 = Female, 1 = Male)"),
        gr.Radio([0, 1], label="Smoking (0 = No, 1 = Yes)"),
        gr.Slider(minimum=4, maximum=285, step=1, label="Follow-up Time (days)"),
    ],
    outputs=gr.Textbox(label="Prediction"),
    title=title,
    description=description,
    allow_flagging='never'
)


# Mount gradio interface object on FastAPI app at endpoint = '/'
app = gr.mount_gradio_app(app, gradio_app, path="/")

app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(root_router)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001) 

    ## local host--> 127.0.0.0  
    ## host --> 0.0.0.0 allows all host

