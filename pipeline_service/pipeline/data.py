from pydantic import BaseModel


class BaseImage(BaseModel):
    image: bytes


class CarDetection(BaseImage):
    top_left_x: int | None = None
    top_left_y: int | None = None
    width: int | None = None
    height: int | None = None
    conf: float | None = None
    label: int | None = None
