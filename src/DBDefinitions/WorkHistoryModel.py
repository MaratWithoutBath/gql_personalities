import datetime
import uuid
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .BaseModel import BaseModel, UUIDFKey, UUIDColumn

class WorkHistoryModel(BaseModel):
    """Represents a record of a user's work history."""

    __tablename__ = "personalitiesworkhistories"

    startdate: Mapped[datetime.datetime] = mapped_column(
        nullable=True, default=True, comment="The start date of the work period"
    )
    enddate: Mapped[datetime.datetime] = mapped_column(
        nullable=True, default=True, comment="The end date of the work period"
    )
    name: Mapped[str] = mapped_column(
        nullable=True, default=True, comment="Name of the workplace or organization"
    )
    ico: Mapped[str] = mapped_column(
        nullable=True, default=True, comment="Organization ICO (Identification Code)"
    )

    user_id: Mapped[uuid.UUID] = UUIDFKey(
        ForeignKey("users.id"), 
        nullable=True, 
        default=True, 
        comment="Foreign Key to the user associated with this work history"
    )
