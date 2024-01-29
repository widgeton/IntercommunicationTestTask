import json
from typing import Type

import database.models as models
from .pipe_settings import DATATYPES, STEPS
from . import steps
from . import data


class Pipeline:
    def __init__(self, pipeline: models.Pipelines):
        self._pipeline = pipeline
        self._steps: dict[int:Type[steps.PipelineStep]] = self._get_steps()
        self._datatype: [Type[data.BaseImage]] = self._get_datatype()

    def _get_steps(self):
        steps = json.loads(self._pipeline.steps)
        steps = {int(k): STEPS.get(v) for k, v in steps.items()}
        return dict(sorted(steps.items(), key=lambda x: x[0]))

    def _get_datatype(self):
        return DATATYPES.get(self._pipeline.datatype)

    async def process(self, image_bytes: bytes):
        data = self._datatype(image=image_bytes)
        for step in self._steps.values():
            data = await step(data).process()
        return data.model_dump()
