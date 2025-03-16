# Setup Python Image
FROM python:3.9-slim

WORKDIR /demo-app

COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

EXPOSE 8000

ENV PYTHONPATH "${PYTHONPATH}:/demo-app"

CMD ["python", "app/main.py"]

