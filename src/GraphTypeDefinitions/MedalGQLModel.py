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
MedalTypeGQLModel = typing.Annotated["MedalTypeGQLModel", strawberry.lazy(".MedalTypeGQLModel")]

@strawberry.federation.type(
    keys=["id"], description="Entity representing a medal awarded to a user"
)
class MedalGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).MedalModel

    startdate: typing.Optional[datetime.datetime] = strawberry.field(
        default=None,
        description="Start date when the medal was awarded",
        permission_classes=[OnlyForAuthentized]
    )
    user_id: typing.Optional[IDType] = strawberry.field(
        default=None,
        description="The ID of the user who received the medal",
        permission_classes=[OnlyForAuthentized]
    )
    medalType_id: typing.Optional[IDType] = strawberry.field(
        default=None,
        description="The ID of the medal type",
        permission_classes=[OnlyForAuthentized]
    )

    user: typing.Optional[UserGQLModel] = strawberry.field(
        description="The user who received the medal",
        permission_classes=[OnlyForAuthentized],
        resolver=ScalarResolver[UserGQLModel](fkey_field_name="user_id")
    )
    medalType: typing.Optional[MedalTypeGQLModel] = strawberry.field(
        description="The type of medal awarded",
        permission_classes=[OnlyForAuthentized],
        resolver=ScalarResolver[MedalTypeGQLModel](fkey_field_name="medalType_id")
    )

@createInputs
@dataclasses.dataclass
class MedalInputFilter:
    startdate: typing.Optional[datetime.datetime] = None
    user_id: typing.Optional[IDType] = None
    medalType_id: typing.Optional[IDType] = None


medal_by_id = strawberry.field(
    description="Find a medal by its ID",
    permission_classes=[OnlyForAuthentized],
    graphql_type=typing.Optional["MedalGQLModel"],
    resolver=MedalGQLModel.load_with_loader
)

medal_page = strawberry.field(
    description="Fetch paginated medals",
    permission_classes=[OnlyForAuthentized],
    resolver=PageResolver["MedalGQLModel"](whereType=MedalInputFilter)
)


@strawberry.input(description="Attributes for creating a medal")
class MedalInsertGQLModel:
    startdate: datetime.datetime = strawberry.field(description="The start date when the medal was awarded")
    user_id: typing.Optional[IDType] = strawberry.field(description="The ID of the user who received the medal", default=None)
    medalType_id: IDType = strawberry.field(description="The ID of the medal type")
    id: typing.Optional[IDType] = strawberry.field(description="Primary key (UUID), can be client-generated", default=None)


@strawberry.input(description="Attributes for updating a medal")
class MedalUpdateGQLModel:
    id: IDType = strawberry.field(description="The primary key of the medal")
    lastchange: datetime.datetime = strawberry.field(description="Timestamp for optimistic locking")

    startdate: typing.Optional[datetime.datetime] = strawberry.field(description="The start date when the medal was awarded", default=None)
    user_id: typing.Optional[IDType] = strawberry.field(description="The ID of the user who received the medal", default=None)
    medalType_id: typing.Optional[IDType] = strawberry.field(description="The ID of the medal type", default=None)


@strawberry.input(description="Attributes needed to delete a medal")
class MedalDeleteGQLModel:
    id: IDType = strawberry.field(description="The primary key of the medal")
    lastchange: datetime.datetime = strawberry.field(description="Timestamp for optimistic locking")


@strawberry.mutation(
    description="Creates a new medal",
    permission_classes=[
        OnlyForAuthentized,
        SimpleInsertPermission[MedalGQLModel](roles=["administrator"]),
    ]
)
async def medal_insert(
    self, info: strawberry.types.Info, medal: MedalInsertGQLModel
) -> typing.Union["MedalGQLModel", InsertError["MedalGQLModel"]]:
    return await Insert["MedalGQLModel"].DoItSafeWay(info=info, entity=medal)


@strawberry.mutation(
    description="Updates an existing medal",
    permission_classes=[
        OnlyForAuthentized,
        SimpleUpdatePermission[MedalGQLModel](roles=["administrator"]),
    ]
)
async def medal_update(
    self, info: strawberry.types.Info, medal: MedalUpdateGQLModel
) -> typing.Union["MedalGQLModel", UpdateError["MedalGQLModel"]]:
    return await Update["MedalGQLModel"].DoItSafeWay(info=info, entity=medal)


@strawberry.mutation(
    description="Deletes a medal",
    permission_classes=[
        OnlyForAuthentized,
        SimpleDeletePermission[MedalGQLModel](roles=["administrator"]),
    ]
)
async def medal_delete(
    self, info: strawberry.types.Info, medal: MedalDeleteGQLModel
) -> typing.Optional[DeleteError["MedalGQLModel"]]:
    return await Delete["MedalGQLModel"].DoItSafeWay(info=info, entity=medal)
