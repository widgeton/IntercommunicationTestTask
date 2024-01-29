from abc import ABC, abstractmethod

import aiohttp
import numpy as np
import cv2
import base64

from pipeline import data
import database.repository as repo
from config import settings


class PipelineStep(ABC):

    @abstractmethod
    async def process(self):
        pass


class CarDetectionStep:
    def __init__(self, data: data.CarDetection):
        self._data = data


class ImageHandler(PipelineStep, CarDetectionStep):
    width = 640
    height = 640

    async def process(self):
        return self._get_processed_image_bytes()

    def _get_processed_image_bytes(self) -> data.CarDetection:
        np_array = np.frombuffer(self._data.image, np.uint8)
        decoded = cv2.imdecode(np_array, -1)
        resized = cv2.resize(decoded, dsize=(self.width, self.height), interpolation=cv2.INTER_AREA)
        normalised = cv2.normalize(resized, np.zeros((self.width, self.height)), 0, 255, cv2.NORM_MINMAX)
        new_image_byte = normalised.tobytes()
        self._data.image = base64.b64encode(new_image_byte)
        return self._data


class MachineLearningModelRequest(PipelineStep, CarDetectionStep):

    async def process(self):
        return await self._request()

    async def _request(self):
        async with aiohttp.ClientSession() as session:
            async with session.post(settings.LEARNING_MACHINE_MODEL_SERVICE_URL,
                                    data={'image': self._data.image}) as response:
                result = await response.json()
                if result is not None:
                    self._data = data.CarDetection(image=self._data.image, **result)
                else:
                    self._data.label = 0
                return self._data


class SaveCarDetection(PipelineStep, CarDetectionStep):

    async def process(self):
        return await self._save()

    async def _save(self):
        await repo.CarDetectionsRepository.save(self._data)
        return self._data
