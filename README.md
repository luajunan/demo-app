# demo-app

A boiler plate for hosting a FastAPI app with an integrated database

## Getting started

```
cd demo-app
pip install -r requirements.txt
```

## Launching the FastAPI App

```
python app/main.py
```

## Launching the monitoring streamlit App

```
streamlit run monitoring_app.py
```

## Running demo-app in Docker

### 1. Build the Docker Image

```
cd demo-app
docker build -t demo-app .
```

### 2. Run the Docker Container

```
docker run -p 8000:8000 demo-app
```

### 3. Stop the Docker Container

```
docker container ls
docker stop <container_id>
```
