from datetime import datetime
from sqlalchemy import ForeignKey, String, DateTime, CHAR, REAL
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base

class SensorData(Base):
    """Sensor-data table
    """
    __tablename__ = "sensor_data"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    device_id: Mapped[str] = mapped_column(String(10))
    sensor_id: Mapped[str] = mapped_column(CHAR)
    time_send: Mapped[datetime] = mapped_column(DateTime)
    time_receive: Mapped[datetime] = mapped_column(DateTime)
    water_content: Mapped[float] = mapped_column(REAL)
    temperature: Mapped[float] = mapped_column(REAL)
