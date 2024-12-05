import uuid
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from .BaseModel import BaseModel, UUIDFKey, UUIDColumn

class CertificateTypeModel(BaseModel):
    """Represents a type of certificate, categorized by a specific group."""

    __tablename__ = "personalitiescertificatetypes"

    name: Mapped[str] = mapped_column(nullable=False, comment="Name of the certificate type", default=None)
    name_en: Mapped[str] = mapped_column(nullable=True, default=None, comment="English name of the certificate type")

    certificateTypeGroup_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("personalitiescertificatecategories.id"), 
        nullable=True, 
        default=None,
        comment="Foreign Key to the certificate category"
    )

    certificates = relationship(
        "CertificateModel", 
        back_populates="certificateType", 
        viewonly=True, 
        uselist=True
    )
    certificateCategory = relationship(
        "CertificateCategoryModel", 
        back_populates="certificateType", 
        viewonly=True
    )
