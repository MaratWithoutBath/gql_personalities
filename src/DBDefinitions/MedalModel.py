import datetime
import uuid
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from .BaseModel import BaseModel, UUIDFKey, UUIDColumn

class MedalModel(BaseModel):
    """Represents a medal awarded to a user."""

    __tablename__ = "personalitiesmedals"

    startdate: Mapped[datetime.datetime] = mapped_column(nullable=False, comment="Year the medal was awarded", default=None)

    user_id: Mapped[uuid.UUID] = UUIDFKey(
        ForeignKey("users.id"),
        nullable=True,
        default=None,
        comment="The user associated with this medal"
    )
    medalType_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("personalitiesmedaltypes.id"),
        nullable=False,
        default=None,
        comment="The type of medal"
    )

    medalType = relationship(
        "MedalTypeModel",
        back_populates="medal",
        viewonly=True
    )
