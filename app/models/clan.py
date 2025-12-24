import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base

class Clan(Base):
    __tablename__ = "clans"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(Text)
    region = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True))