FROM python:alpine
WORKDIR /service
COPY . .
RUN pip install --no-cache-dir -r ./requirements.txt
CMD uvicorn service:app --host 0.0.0.0 --port 8002