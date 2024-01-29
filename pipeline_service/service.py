
from fastapi import FastAPI, UploadFile
from contextlib import asynccontextmanager
from uuid import UUID

import database.repository as repo
import pipeline.pipeline as pipe
import database.db as db


@asynccontextmanager
async def lifespan(app: FastAPI):
    db.create_tables()
    await repo.PipelineRepository.create_fake_pipline()
    yield


app = FastAPI(lifespan=lifespan)


@app.post('/process_image/')
async def process_image(image: UploadFile, pipeline_id: UUID):
    pipeline = await repo.PipelineRepository.get_pipeline(pipeline_id)
    image_bytes = await image.read()
    pipeline = pipe.Pipeline(pipeline)
    await pipeline.process(image_bytes)
    return {'message': 'success'}
