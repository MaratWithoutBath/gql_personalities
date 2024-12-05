import sqlalchemy
import datetime
import uuid
from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .BaseModel import BaseModel, UUIDFKey, UUIDColumn

class StudyModel(BaseModel):
    __tablename__ = "personalitiesstudies"

    name: Mapped[str] = mapped_column(nullable=True, default=None, comment="Name of the study")
    name_en: Mapped[str] = mapped_column(nullable=True, default=None, comment="English name of the study")
    program: Mapped[str] = mapped_column(nullable=True, default=None, comment="Program of the study")
    startdate: Mapped[datetime.datetime] = mapped_column(nullable=True, default=None, comment="Start date and time of the study")
    enddate: Mapped[datetime.datetime] = mapped_column(nullable=True, default=None, comment="End date and time of the study")

    user_id: Mapped[uuid.UUID] = UUIDFKey(ForeignKey("users.id"), nullable=True, index=True, comment="ID of the user associated with this study")
