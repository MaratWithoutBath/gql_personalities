import uuid
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from .BaseModel import BaseModel, UUIDFKey, UUIDColumn

class MedalTypeModel(BaseModel):
    """Represents the type of a medal."""

    __tablename__ = "personalitiesmedaltypes"

    name: Mapped[str] = mapped_column(nullable=False, default=None, comment="Name of the medal type")
    name_en: Mapped[str] = mapped_column(nullable=True, default=None, comment="English name of the medal type")

    medalTypeGroup_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("personalitiesmedalcategories.id"),
        nullable=True,
        default=None,
        comment="Foreign Key to the medal type group"
    )

    medal = relationship(
        "MedalModel",
        back_populates="medalType",
        viewonly=True,
        uselist=True
    )
    medalCategory = relationship(
        "MedalCategoryModel",
        back_populates="medalTypes",
        viewonly=True
    )
