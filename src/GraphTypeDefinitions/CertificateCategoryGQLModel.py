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
    VectorResolver,
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

CertificateTypeGQLModel = typing.Annotated["CertificateTypeGQLModel", strawberry.lazy(".CertificateTypeGQLModel")]

@strawberry.federation.type(
    keys=["id"], description="Entity representing a certificate type group"
)
class CertificateCategoryGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).CertificateCategoryModel

    name: typing.Optional[str] = strawberry.field(
        default=None,
        description="The name of the certificate type group",
        permission_classes=[OnlyForAuthentized]
    )
    name_en: typing.Optional[str] = strawberry.field(
        default=None,
        description="The English name of the certificate type group",
        permission_classes=[OnlyForAuthentized]
    )
    changedby_id: typing.Optional[IDType] = strawberry.field(
        default=None,
        description="ID of the user who last changed the group",
        permission_classes=[OnlyForAuthentized]
    )

    certificates: typing.List[CertificateTypeGQLModel] = strawberry.field(
        description="List of certificate types associated with this group",
        permission_classes=[OnlyForAuthentized],
        resolver=VectorResolver[CertificateTypeGQLModel](fkey_field_name="certificateTypeGroup_id", whereType=None)
    )

# @createInputs
# @dataclasses.dataclass
# class CertificateTypeGroupInputFilter:
#     name: typing.Optional[str] = None
#     name_en: typing.Optional[str] = None
#     changedby_id: typing.Optional[IDType] = None
#     created: typing.Optional[datetime.datetime] = None
#     lastchange: typing.Optional[datetime.datetime] = None

@createInputs
@dataclasses.dataclass
class CertificateTypeGroupInputFilter:
    name: str
    name_en: str
    changedby_id: IDType
    created: datetime.datetime
    lastchange: datetime.datetime

certificate_category_page = strawberry.field(
    description="Fetch paginated certificate type groups",
    permission_classes=[OnlyForAuthentized],
    resolver=PageResolver["CertificateCategoryGQLModel"](whereType=CertificateTypeGroupInputFilter)
)
certificate_category_by_id = strawberry.field(
    description="Find a certificate type group by its ID",
    permission_classes=[OnlyForAuthentized],
    graphql_type=typing.Optional["CertificateCategoryGQLModel"],
    resolver=CertificateCategoryGQLModel.load_with_loader
)

@strawberry.input(description="Attributes for creating a certificate type group")
class CertificateTypeGroupInsertGQLModel:
    name: str = strawberry.field(description="The name of the certificate type group")
    name_en: typing.Optional[str] = strawberry.field(
        description="The English name of the certificate type group", default=None
    )
    id: typing.Optional[IDType] = strawberry.field(
        description="Primary key (UUID), can be client-generated", default=None
    )
    changedby_id: typing.Optional[IDType] = strawberry.field(
        description="The user who created this certificate type group", default=None
    )


@strawberry.input(description="Attributes for updating a certificate type group")
class CertificateTypeGroupUpdateGQLModel:
    id: IDType = strawberry.field(description="The primary key of the certificate type group")
    lastchange: datetime.datetime = strawberry.field(description="Timestamp for optimistic locking")

    name: typing.Optional[str] = strawberry.field(description="The name of the certificate type group", default=None)
    name_en: typing.Optional[str] = strawberry.field(
        description="The English name of the certificate type group", default=None
    )
    changedby_id: typing.Optional[IDType] = strawberry.field(
        description="The user who last modified this certificate type group", default=None
    )


@strawberry.input(description="Attributes needed to delete a certificate type group")
class CertificateTypeGroupDeleteGQLModel:
    id: IDType = strawberry.field(description="The primary key of the certificate type group")
    lastchange: datetime.datetime = strawberry.field(description="Timestamp for optimistic locking")


@strawberry.mutation(
    description="Creates a new certificate type group",
    permission_classes=[
        OnlyForAuthentized,
        SimpleInsertPermission[CertificateCategoryGQLModel](roles=["administrátor"]),
    ]
)
async def certificate_type_group_insert(
    self, info: strawberry.types.Info, certificate_type_group: CertificateTypeGroupInsertGQLModel
) -> typing.Union["CertificateCategoryGQLModel", InsertError["CertificateCategoryGQLModel"]]:
    return await Insert[CertificateCategoryGQLModel].DoItSafeWay(info=info, entity=certificate_type_group)


@strawberry.mutation(
    description="Updates an existing certificate type group",
    permission_classes=[
        OnlyForAuthentized,
        SimpleUpdatePermission[CertificateCategoryGQLModel](roles=["administrátor"]),
    ]
)
async def certificate_type_group_update(
    self, info: strawberry.types.Info, certificate_type_group: CertificateTypeGroupUpdateGQLModel
) -> typing.Union["CertificateCategoryGQLModel", UpdateError["CertificateCategoryGQLModel"]]:
    return await Update[CertificateCategoryGQLModel].DoItSafeWay(info=info, entity=certificate_type_group)


@strawberry.mutation(
    description="Deletes a certificate type group",
    permission_classes=[
        OnlyForAuthentized,
        SimpleDeletePermission[CertificateCategoryGQLModel](roles=["administrátor"]),
    ]
)
async def certificate_type_group_delete(
    self, info: strawberry.types.Info, certificate_type_group: CertificateTypeGroupDeleteGQLModel
) -> typing.Optional[DeleteError[CertificateCategoryGQLModel]]:
    return await Delete[CertificateCategoryGQLModel].DoItSafeWay(info=info, entity=certificate_type_group)
