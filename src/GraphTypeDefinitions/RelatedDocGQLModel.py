import dataclasses
import datetime
import typing
import strawberry

from uoishelpers.gqlpermissions import (
    OnlyForAuthentized,
    SimpleInsertPermission,
    SimpleUpdatePermission,
    SimpleDeletePermission
)
from uoishelpers.resolvers import (
    getLoadersFromInfo,
    ScalarResolver,
    PageResolver,
    InsertError,
    Insert,
    UpdateError,
    Update,
    DeleteError,
    Delete,
    createInputs
)

from .BaseGQLModel import BaseGQLModel, IDType

UserGQLModel = typing.Annotated["UserGQLModel", strawberry.lazy(".UserGQLModel")]

@strawberry.federation.type(
    keys=["id"], description="Entity representing a related document associated with a user"
)
class RelatedDocGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).RelatedDocModel

    name: typing.Optional[str] = strawberry.field(
        default=None,
        description="Name or title of the document",
        permission_classes=[OnlyForAuthentized]
    )
    document: typing.Optional[str] = strawberry.field(
        default=None,
        description="Binary data of the uploaded document",
        permission_classes=[OnlyForAuthentized]
    )
    document_mime_type: typing.Optional[str] = strawberry.field(
        default=None,
        description="MIME type of the uploaded document (e.g., application/pdf)",
        permission_classes=[OnlyForAuthentized]
    )
    user_id: typing.Optional[IDType] = strawberry.field(
        default=None,
        description="The ID of the user associated with this document",
        permission_classes=[OnlyForAuthentized]
    )
    # user: typing.Optional[UserGQLModel] = strawberry.field(
    #     description="The user associated with this document",
    #     permission_classes=[OnlyForAuthentized],
    #     resolver=ScalarResolver[UserGQLModel](fkey_field_name="user_id")
    # )


@createInputs
@dataclasses.dataclass
class RelatedDocInputFilter:
    name: typing.Optional[str] = None
    document_mime_type: typing.Optional[str] = None
    user_id: typing.Optional[IDType] = None


related_doc_by_id = strawberry.field(
    description="Find a related document by its ID",
    permission_classes=[OnlyForAuthentized],
    graphql_type=typing.Optional[RelatedDocGQLModel],
    resolver=RelatedDocGQLModel.load_with_loader
)

related_doc_page = strawberry.field(
    description="Fetch paginated related documents",
    permission_classes=[OnlyForAuthentized],
    resolver=PageResolver[RelatedDocGQLModel](whereType=RelatedDocInputFilter)
)

@strawberry.input(description="Attributes for creating a related document")
class RelatedDocInsertGQLModel:
    name: str = strawberry.field(description="Name or title of the document")
    document: typing.Optional[str] = strawberry.field(description="Binary data of the uploaded document", default=None)
    document_mime_type: typing.Optional[str] = strawberry.field(description="MIME type of the uploaded document (e.g., application/pdf)", default=None)
    user_id: typing.Optional[IDType] = strawberry.field(description="The ID of the user associated with this document", default=None)
    id: typing.Optional[IDType] = strawberry.field(description="Primary key (UUID), can be client-generated", default=None)


@strawberry.input(description="Attributes for updating a related document")
class RelatedDocUpdateGQLModel:
    id: IDType = strawberry.field(description="The primary key of the related document")
    lastchange: typing.Optional[datetime.datetime] = strawberry.field(description="Timestamp for optimistic locking")

    name: typing.Optional[str] = strawberry.field(description="Name or title of the document", default=None)
    document: typing.Optional[str] = strawberry.field(description="Binary data of the uploaded document", default=None)
    document_mime_type: typing.Optional[str] = strawberry.field(description="MIME type of the uploaded document (e.g., application/pdf)", default=None)
    user_id: typing.Optional[IDType] = strawberry.field(description="The ID of the user associated with this document", default=None)


@strawberry.input(description="Attributes needed to delete a related document")
class RelatedDocDeleteGQLModel:
    id: IDType = strawberry.field(description="The primary key of the related document")
    lastchange: typing.Optional[str] = strawberry.field(description="Timestamp for optimistic locking")


@strawberry.mutation(
    description="Creates a new related document",
    permission_classes=[
        OnlyForAuthentized,
        SimpleInsertPermission[RelatedDocGQLModel](roles=["administrator"]),
    ]
)
async def related_doc_insert(
    self, info: strawberry.types.Info, related_doc: RelatedDocInsertGQLModel
) -> typing.Union[RelatedDocGQLModel, InsertError[RelatedDocGQLModel]]:
    return await Insert[RelatedDocGQLModel].DoItSafeWay(info=info, entity=related_doc)


@strawberry.mutation(
    description="Updates an existing related document",
    permission_classes=[
        OnlyForAuthentized,
        SimpleUpdatePermission[RelatedDocGQLModel](roles=["administrator"]),
    ]
)
async def related_doc_update(
    self, info: strawberry.types.Info, related_doc: RelatedDocUpdateGQLModel
) -> typing.Union[RelatedDocGQLModel, UpdateError[RelatedDocGQLModel]]:
    return await Update[RelatedDocGQLModel].DoItSafeWay(info=info, entity=related_doc)


@strawberry.mutation(
    description="Deletes a related document",
    permission_classes=[
        OnlyForAuthentized,
        SimpleDeletePermission[RelatedDocGQLModel](roles=["administrator"]),
    ]
)
async def related_doc_delete(
    self, info: strawberry.types.Info, related_doc: RelatedDocDeleteGQLModel
) -> typing.Optional[DeleteError[RelatedDocGQLModel]]:
    return await Delete[RelatedDocGQLModel].DoItSafeWay(info=info, entity=related_doc)
