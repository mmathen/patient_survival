# pull python base image
FROM python:3.10

# specify working directory
WORKDIR /patient_survival_model_api

#ADD /patient_survival_model_api/requirements.txt .
COPY /patient_survival_model_api/requirements.txt .
#ADD /patient_survival_model_api/*.whl .
COPY /patient_survival_model_api/*.whl .

# update pip
RUN pip install --upgrade pip

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt


RUN rm *.whl

# copy application files
#ADD /patient_survival_model_api/app/* ./app/
COPY /patient_survival_model_api/app/* ./app/

# expose port for application
EXPOSE 8001

# start fastapi application
CMD ["python", "app/main.py"]
