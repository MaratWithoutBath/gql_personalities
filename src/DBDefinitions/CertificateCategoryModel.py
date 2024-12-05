import datetime
import uuid
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from .BaseModel import BaseModel, UUIDFKey, UUIDColumn

class CertificateCategoryModel(BaseModel):
    """Represents a category group for certificate types."""

    __tablename__ = "personalitiescertificatecategories"

    name: Mapped[str] = mapped_column(nullable=False, default=None, comment="Name of the certificate type group")
    name_en: Mapped[str] = mapped_column(nullable=True, default=None, comment="English name of the certificate type group")

    certificateType = relationship(
        "CertificateTypeModel",
        back_populates="certificateCategory",
        uselist=True,
        viewonly=True
    )
