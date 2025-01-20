# Standard libraries
import dataclasses
import datetime
import typing
import uuid

# Strawberry library for GraphQL
import strawberry

# Permissions from project helpers
from uoishelpers.gqlpermissions import (
    OnlyForAuthentized,          # Restricts access to authenticated users
    SimpleInsertPermission,      # For role-based insert permission
    SimpleUpdatePermission,      # For role-based update permission
    SimpleDeletePermission       # For role-based delete permission
)

# Resolvers from project helpers
from uoishelpers.resolvers import (
    getLoadersFromInfo,          # Loads data using DataLoader
    InsertError,                 # Error type for insert mutations
    Insert,                      # Insert resolver utility
    UpdateError,                 # Error type for update mutations
    Update,                      # Update resolver utility
    DeleteError,                 # Error type for delete mutations
    Delete,                      # Delete resolver utility
    PageResolver,                # Paged query resolver utility
    ScalarResolver               # Resolver for scalar relationships
)

# Base GQL Model for GraphQL type inheritance
from .BaseGQLModel import BaseGQLModel, IDType

# Import related GraphQL models
UserGQLModel = typing.Annotated["UserGQLModel", strawberry.lazy(".UserGQLModel")]
CertificateTypeGQLModel = typing.Annotated["CertificateTypeGQLModel", strawberry.lazy(".CertificateTypeGQLModel")]

# Input generation utility
from uoishelpers.resolvers import createInputs


UserGQLModel = typing.Annotated["UserGQLModel", strawberry.lazy(".UserGQLModel")]
CertificateTypeGQLModel = typing.Annotated["CertificateTypeGQLModel", strawberry.lazy(".CertificateTypeGQLModel")]

@strawberry.federation.type(
    keys=["id"], description="Entity representing a certificate"
)
class CertificateGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).CertificateModel

    level: typing.Optional[str] = strawberry.field(
        default=None,
        description="Certificate level",
        permission_classes=[OnlyForAuthentized]
    )
    startdate: typing.Optional[datetime.datetime] = strawberry.field(
        default=None,
        description="Start date of certificate validity",
        permission_classes=[OnlyForAuthentized]
    )
    enddate: typing.Optional[datetime.datetime] = strawberry.field(
        default=None,
        description="End date of certificate validity",
        permission_classes=[OnlyForAuthentized]
    )

    user_id: typing.Optional[IDType] = strawberry.field(
        default=None,
        description="User ID associated with this certificate",
        permission_classes=[OnlyForAuthentized]
    )
    certificateType_id: typing.Optional[IDType] = strawberry.field(
        default=None,
        description="Type ID of the certificate",
        permission_classes=[OnlyForAuthentized]
    )

    certificateType: typing.Optional[CertificateTypeGQLModel] = strawberry.field(
        description="Type of the certificate",
        permission_classes=[OnlyForAuthentized],
        resolver=ScalarResolver["CertificateTypeGQLModel"](fkey_field_name="certificateType_id")
    )
    user: typing.Optional[UserGQLModel] = strawberry.field(
        description="owner",
        permission_classes=[OnlyForAuthentized],
        resolver=ScalarResolver[UserGQLModel](fkey_field_name="user_id")
    )


@createInputs
@dataclasses.dataclass
class CertificateInputFilter:
    level: typing.Optional[str] = None
    startdate: typing.Optional[datetime.datetime] = None
    enddate: typing.Optional[datetime.datetime] = None
    user_id: typing.Optional[IDType] = None
    certificateType_id: typing.Optional[IDType] = None


certificate_by_id = strawberry.field(
    description="Find a certificate by its ID",
    permission_classes=[OnlyForAuthentized],
    graphql_type=typing.Optional[CertificateGQLModel],
    resolver=CertificateGQLModel.load_with_loader
)

certificate_page = strawberry.field(
    description="Fetch paged certificates",
    permission_classes=[OnlyForAuthentized],
    resolver=PageResolver[CertificateGQLModel](whereType=CertificateInputFilter)
)

@strawberry.input(description="Attributes for creating a certificate")
class CertificateInsertGQLModel:
    level: str = strawberry.field(description="The level of the certificate")
    startdate: typing.Optional[datetime.datetime] = strawberry.field(
        description="Start date of the certificate validity", default=None
    )
    enddate: typing.Optional[datetime.datetime] = strawberry.field(
        description="End date of the certificate validity", default=None
    )
    user_id: typing.Optional[IDType] = strawberry.field(
        description="The ID of the user associated with the certificate", default=None
    )
    certificateType_id: typing.Optional[IDType] = strawberry.field(
        description="The ID of the certificate type", default=None
    )
    id: typing.Optional[IDType] = strawberry.field(
        description="Primary key (UUID), can be client-generated", default=None
    )


@strawberry.input(description="Attributes for updating a certificate")
class CertificateUpdateGQLModel:
    id: IDType = strawberry.field(description="The primary key of the certificate")
    lastchange: datetime.datetime = strawberry.field(
        description="Timestamp for optimistic locking"
    )

    level: typing.Optional[str] = strawberry.field(description="The level of the certificate", default=None)
    startdate: typing.Optional[datetime.datetime] = strawberry.field(
        description="Start date of the certificate validity", default=None
    )
    enddate: typing.Optional[datetime.datetime] = strawberry.field(
        description="End date of the certificate validity", default=None
    )
    user_id: typing.Optional[IDType] = strawberry.field(
        description="The ID of the user associated with the certificate", default=None
    )
    certificateType_id: typing.Optional[IDType] = strawberry.field(
        description="The ID of the certificate type", default=None
    )


@strawberry.input(description="Attributes needed to delete a certificate")
class CertificateDeleteGQLModel:
    id: IDType = strawberry.field(description="The primary key of the certificate")
    lastchange: datetime.datetime = strawberry.field(
        description="Timestamp for optimistic locking"
    )


@strawberry.mutation(
    description="Creates a new certificate",
    permission_classes=[
        OnlyForAuthentized,
        SimpleInsertPermission[CertificateGQLModel](roles=["administrátor"]),
    ]
)
async def certificate_insert(
    self, info: strawberry.types.Info, certificate: CertificateInsertGQLModel
) -> typing.Union[CertificateGQLModel, InsertError[CertificateGQLModel]]:
    return await Insert[CertificateGQLModel].DoItSafeWay(info=info, entity=certificate)


@strawberry.mutation(
    description="Updates an existing certificate",
    permission_classes=[
        OnlyForAuthentized,
        SimpleUpdatePermission[CertificateGQLModel](roles=["administrátor"]),
    ]
)
async def certificate_update(
    self, info: strawberry.types.Info, certificate: CertificateUpdateGQLModel
) -> typing.Union[CertificateGQLModel, UpdateError[CertificateGQLModel]]:
    return await Update[CertificateGQLModel].DoItSafeWay(info=info, entity=certificate)


@strawberry.mutation(
    description="Deletes a certificate",
    permission_classes=[
        OnlyForAuthentized,
        SimpleDeletePermission[CertificateGQLModel](roles=["administrátor"]),
    ]
)
async def certificate_delete(
    self, info: strawberry.types.Info, certificate: CertificateDeleteGQLModel
) -> typing.Optional[DeleteError[CertificateGQLModel]]:
    return await Delete[CertificateGQLModel].DoItSafeWay(info=info, entity=certificate)
