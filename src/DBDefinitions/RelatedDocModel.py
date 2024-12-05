import uuid
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .BaseModel import BaseModel, UUIDFKey, UUIDColumn

class RelatedDocModel(BaseModel):
    """Represents a document related to a user."""

    __tablename__ = "personalitiesrelateddocs"

    name: Mapped[str] = mapped_column(
        nullable=False, 
        default=True, 
        comment="Name or title of the document"
    )
    document: Mapped[bytes] = mapped_column(
        nullable=True, 
        default=True, 
        comment="Binary data for the uploaded document"
    )
    document_mime_type: Mapped[str] = mapped_column(
        nullable=True,
        default=True,  
        comment="MIME type of the uploaded document (e.g., application/pdf)"
    )

    user_id: Mapped[uuid.UUID] = UUIDFKey(
        ForeignKey("users.id"),
        nullable=True,
        comment="Foreign Key to the user associated with this document"
    )
