import datetime
import uuid
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from .BaseModel import BaseModel, UUIDFKey, UUIDColumn

class CertificateModel(BaseModel):
    """Represents certificates associated with users and types."""

    __tablename__ = "personalitiescertificates"

    level: Mapped[str] = mapped_column(nullable=True, default=None, comment="Certificate level")
    startdate: Mapped[datetime.datetime] = mapped_column(nullable=True, default=None, comment="Start date of validity")
    enddate: Mapped[datetime.datetime] = mapped_column(nullable=True, default=None, comment="End date of validity")

    user_id: Mapped[uuid.UUID] = UUIDFKey(ForeignKey("users.id"), nullable=True, default=None, comment="User associated with this certificate")
    certificateType_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("personalitiescertificatetypes.id"), nullable=True, default=None, comment="Type of certificate")

    certificateType = relationship("CertificateTypeModel", back_populates="certificates", viewonly=True)
