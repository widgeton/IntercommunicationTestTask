import json
from uuid import UUID
from sqlalchemy import select

from . import db
from . import models
import pipeline.data as data


class PipelineRepository:
    @staticmethod
    async def get_pipeline(id: UUID):
        async with db.AsyncSession() as session:
            query = select(models.Pipelines).filter_by(id=id)
            pipeline = await session.execute(query)
            return pipeline.scalars().first()

    @staticmethod
    async def create_fake_pipline():
        async with db.AsyncSession() as session:
            steps = {1: 'ImageHandler', 2: 'MachineLearningModelRequest', 3: 'SaveCarDetection'}
            session.add(models.Pipelines(id='146bde7b-2e23-447f-84e3-b1d6f7045b62',
                                         description="Обнаружение автомобилей",
                                         steps=json.dumps(steps),
                                         datatype='CarDetection'))
            await session.commit()


class CarDetectionsRepository:
    @staticmethod
    async def save(instance: data.CarDetection):
        async with db.AsyncSession() as session:
            session.add(models.CarDetections(**instance.model_dump()))
            await session.commit()
