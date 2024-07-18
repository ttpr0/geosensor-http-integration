from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base

META_DATA: MetaData = MetaData()

Base = declarative_base(metadata=META_DATA)

from .sensor import SensorData
