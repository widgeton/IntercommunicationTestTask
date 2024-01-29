import uuid

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from typing import Annotated

from config import settings

DB_URL = settings.db_url()
engine = create_engine(DB_URL)
Session = sessionmaker(engine, autoflush=False)

async_engine = create_async_engine(DB_URL)
AsyncSession = async_sessionmaker(async_engine, autoflush=False)

pk = Annotated[str, mapped_column(nullable=False, unique=True, primary_key=True, default=uuid.uuid4)]


class Base(DeclarativeBase):
    type_annotation_map = {
        pk: UUID(as_uuid=True),
    }


def create_tables():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
