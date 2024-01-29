from sqlalchemy.orm import Mapped

from .db import Base, pk


class Pipelines(Base):
    __tablename__ = 'pipelines'

    id: Mapped[pk]
    description: Mapped[str]
    steps: Mapped[str]
    datatype: Mapped[str]


class CarDetections(Base):
    __tablename__ = 'car_detections'

    id: Mapped[pk]
    image: Mapped[str]
    top_left_x: Mapped[int | None]
    top_left_y: Mapped[int | None]
    width: Mapped[int | None]
    height: Mapped[int | None]
    conf: Mapped[float | None]
    label: Mapped[int | None]
