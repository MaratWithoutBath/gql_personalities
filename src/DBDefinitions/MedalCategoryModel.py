import uuid
from sqlalchemy.orm import relationship, Mapped, mapped_column

from .BaseModel import BaseModel, UUIDColumn

class MedalCategoryModel(BaseModel):
    """Represents a category for medal types."""

    __tablename__ = "personalitiesmedalcategories"

    name: Mapped[str] = mapped_column(nullable=False, default=None, comment="Name of the medal category")
    name_en: Mapped[str] = mapped_column(nullable=True, default=None, comment="English name of the medal category")

    medalTypes = relationship(
        "MedalTypeModel",
        back_populates="medalCategory",
        viewonly=True,
        uselist=True
    )
