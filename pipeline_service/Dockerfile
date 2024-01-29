FROM python
WORKDIR /service
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y && apt-get clean
COPY . .
RUN pip install --no-cache-dir -r ./requirements.txt
CMD uvicorn service:app --host 0.0.0.0 --port 8001