import sqlalchemy
import datetime
import uuid
from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .BaseModel import BaseModel, UUIDFKey, UUIDColumn

class RankTypeModel(BaseModel):
    __tablename__ = "personalitiesranktypes"

    name: Mapped[str] = mapped_column(nullable=False, default=None, comment="")
    name_en: Mapped[str] = mapped_column(nullable=False, default=None, comment="")

    rank = relationship("RankModel", back_populates="rank_type")
