import sqlalchemy
import datetime
import uuid
from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .BaseModel import BaseModel, UUIDFKey, UUIDColumn

class RankModel(BaseModel):
    __tablename__ = "personalitiesranks"

    startdate: Mapped[datetime.datetime] = mapped_column(default=None, nullable=True, comment="")
    enddate: Mapped[datetime.datetime] = mapped_column(default=None, nullable=True, comment="")

    user_id: Mapped[uuid.UUID] = UUIDFKey(nullable=True)  # ForeignKey("users.id"), index=True
    ranktype_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("personalitiesranktypes.id"), index=True, default=None, nullable=True)

    rank_type = relationship("RankTypeModel", back_populates="rank")
