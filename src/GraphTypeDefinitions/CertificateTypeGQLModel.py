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
    InsertError,
    Insert,
    UpdateError,
    Update,
    DeleteError,
    Delete,
    PageResolver,
    ScalarResolver,
    VectorResolver,
    createInputs
)

from .BaseGQLModel import BaseGQLModel, IDType

CertificateGQLModel = typing.Annotated["CertificateGQLModel", strawberry.lazy(".CertificateGQLModel")]
CertificateCategoryGQLModel = typing.Annotated["CertificateCategoryGQLModel", strawberry.lazy(".CertificateCategoryGQLModel")]

# Define the GraphQL model
@strawberry.federation.type(
    keys=["id"], description="Entity representing a certificate type"
)
class CertificateTypeGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).CertificateTypeModel

    name: typing.Optional[str] = strawberry.field(
        default=None,
        description="The name of the certificate type",
        permission_classes=[OnlyForAuthentized]
    )
    name_en: typing.Optional[str] = strawberry.field(
        default=None,
        description="The English name of the certificate type",
        permission_classes=[OnlyForAuthentized]
    )
    certificateTypeGroup_id: typing.Optional[IDType] = strawberry.field(
        default=None,
        description="The ID of the certificate category group",
        permission_classes=[OnlyForAuthentized]
    )

    certificateTypeGroup: typing.Optional[CertificateCategoryGQLModel] = strawberry.field(
        description="The group this certificate type belongs to",
        permission_classes=[OnlyForAuthentized],
        resolver=ScalarResolver["CertificateTypeGroupGQLModel"](fkey_field_name="certificateTypeGroup_id")
    )

    certificates: typing.List[CertificateGQLModel] = strawberry.field(
        description="Certificates associated with this type",
        permission_classes=[OnlyForAuthentized],
        resolver=VectorResolver[CertificateGQLModel](fkey_field_name="certificateType_id", whereType=None)
    )


@createInputs
@dataclasses.dataclass
class CertificateTypeInputFilter:
    name: typing.Optional[str] = None
    name_en: typing.Optional[str] = None
    certificateTypeGroup_id: typing.Optional[IDType] = None


certificate_type_by_id = strawberry.field(
    description="Find a certificate type by its ID",
    permission_classes=[OnlyForAuthentized],
    graphql_type=typing.Optional[CertificateTypeGQLModel],
    resolver=CertificateTypeGQLModel.load_with_loader
)

certificate_type_page = strawberry.field(
    description="Fetch paged certificate types",
    permission_classes=[OnlyForAuthentized],
    resolver=PageResolver[CertificateTypeGQLModel](whereType=CertificateTypeInputFilter)
)


@strawberry.input(description="Attributes for creating a certificate type")
class CertificateTypeInsertGQLModel:
    name: str = strawberry.field(description="The name of the certificate type")
    name_en: typing.Optional[str] = strawberry.field(description="The English name of the certificate type", default=None)
    certificateTypeGroup_id: typing.Optional[IDType] = strawberry.field(description="The ID of the certificate category group", default=None)
    id: typing.Optional[IDType] = strawberry.field(description="Primary key (UUID), can be client-generated", default=None)


@strawberry.input(description="Attributes for updating a certificate type")
class CertificateTypeUpdateGQLModel:
    id: IDType = strawberry.field(description="The primary key of the certificate type")
    lastchange: datetime.datetime = strawberry.field(description="Timestamp for optimistic locking")

    name: typing.Optional[str] = strawberry.field(description="The name of the certificate type", default=None)
    name_en: typing.Optional[str] = strawberry.field(description="The English name of the certificate type", default=None)
    certificateTypeGroup_id: typing.Optional[IDType] = strawberry.field(description="The ID of the certificate category group", default=None)


@strawberry.input(description="Attributes needed to delete a certificate type")
class CertificateTypeDeleteGQLModel:
    id: IDType = strawberry.field(description="The primary key of the certificate type")
    lastchange: datetime.datetime = strawberry.field(description="Timestamp for optimistic locking")


@strawberry.mutation(
    description="Creates a new certificate type",
    permission_classes=[
        OnlyForAuthentized,
        SimpleInsertPermission[CertificateTypeGQLModel](roles=["administrator"]),
    ]
)
async def certificate_type_insert(
    self, info: strawberry.types.Info, certificate_type: CertificateTypeInsertGQLModel
) -> typing.Union[CertificateTypeGQLModel, InsertError[CertificateTypeGQLModel]]:
    return await Insert[CertificateTypeGQLModel].DoItSafeWay(info=info, entity=certificate_type)


@strawberry.mutation(
    description="Updates an existing certificate type",
    permission_classes=[
        OnlyForAuthentized,
        SimpleUpdatePermission[CertificateTypeGQLModel](roles=["administrator"]),
    ]
)
async def certificate_type_update(
    self, info: strawberry.types.Info, certificate_type: CertificateTypeUpdateGQLModel
) -> typing.Union[CertificateTypeGQLModel, UpdateError[CertificateTypeGQLModel]]:
    return await Update[CertificateTypeGQLModel].DoItSafeWay(info=info, entity=certificate_type)


@strawberry.mutation(
    description="Deletes a certificate type",
    permission_classes=[
        OnlyForAuthentized,
        SimpleDeletePermission[CertificateTypeGQLModel](roles=["administrator"]),
    ]
)
async def certificate_type_delete(
    self, info: strawberry.types.Info, certificate_type: CertificateTypeDeleteGQLModel
) -> typing.Optional[DeleteError[CertificateTypeGQLModel]]:
    return await Delete[CertificateTypeGQLModel].DoItSafeWay(info=info, entity=certificate_type)
