FROM python:3.8
EXPOSE 8080
WORKDIR /app
COPY . ./
RUN pip install -r requirements.txt && apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
ENTRYPOINT ["streamlit", "run", "Sign_In.py", "--server.port=8080", "--server.address=0.0.0.0"]