FROM python:3.8
EXPOSE 8080
ARG GOOGLE_APPLICATION_CREDENTIALS="./application_default_credentials.json"
WORKDIR /app
COPY . ./
RUN pip install -r requirements.txt && apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]