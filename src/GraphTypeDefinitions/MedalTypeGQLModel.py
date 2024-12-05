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
    VectorResolver,
    InsertError,
    Insert,
    UpdateError,
    Update,
    DeleteError,
    Delete,
    createInputs
)

from .BaseGQLModel import BaseGQLModel, IDType

MedalGQLModel = typing.Annotated["MedalGQLModel", strawberry.lazy(".MedalGQLModel")]
MedalCategoryGQLModel = typing.Annotated["MedalCategoryGQLModel", strawberry.lazy(".MedalCategoryGQLModel")]

@strawberry.federation.type(
    keys=["id"], description="Entity representing a type of medal"
)
class MedalTypeGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).MedalTypeModel

    name: typing.Optional[str] = strawberry.field(
        default=None,
        description="The name of the medal type",
        permission_classes=[OnlyForAuthentized]
    )
    name_en: typing.Optional[str] = strawberry.field(
        default=None,
        description="The English name of the medal type",
        permission_classes=[OnlyForAuthentized]
    )
    medalTypeGroup_id: typing.Optional[IDType] = strawberry.field(
        default=None,
        description="The ID of the medal type group",
        permission_classes=[OnlyForAuthentized]
    )

    medals: typing.List[MedalGQLModel] = strawberry.field(
        description="Medals associated with this medal type",
        permission_classes=[OnlyForAuthentized],
        resolver=VectorResolver[MedalGQLModel](fkey_field_name="medalType_id", whereType=None)
    )
    medalTypeGroup: typing.Optional[MedalCategoryGQLModel] = strawberry.field(
        description="The group this medal type belongs to",
        permission_classes=[OnlyForAuthentized],
        resolver=ScalarResolver[MedalCategoryGQLModel](fkey_field_name="medalTypeGroup_id")
    )


@createInputs
@dataclasses.dataclass
class MedalTypeInputFilter:
    name: typing.Optional[str] = None
    name_en: typing.Optional[str] = None
    medalTypeGroup_id: typing.Optional[IDType] = None


medal_type_by_id = strawberry.field(
    description="Find a medal type by its ID",
    permission_classes=[OnlyForAuthentized],
    graphql_type=typing.Optional[MedalTypeGQLModel],
    resolver=MedalTypeGQLModel.load_with_loader
)

medal_type_page = strawberry.field(
    description="Fetch paginated medal types",
    permission_classes=[OnlyForAuthentized],
    resolver=PageResolver[MedalTypeGQLModel](whereType=MedalTypeInputFilter)
)


@strawberry.input(description="Attributes for creating a medal type")
class MedalTypeInsertGQLModel:
    name: str = strawberry.field(description="The name of the medal type")
    name_en: typing.Optional[str] = strawberry.field(description="The English name of the medal type", default=None)
    medalTypeGroup_id: IDType = strawberry.field(description="The ID of the medal type group")
    id: typing.Optional[IDType] = strawberry.field(description="Primary key (UUID), can be client-generated", default=None)


@strawberry.input(description="Attributes for updating a medal type")
class MedalTypeUpdateGQLModel:
    id: IDType = strawberry.field(description="The primary key of the medal type")
    lastchange: datetime.datetime = strawberry.field(description="Timestamp for optimistic locking")

    name: typing.Optional[str] = strawberry.field(description="The name of the medal type", default=None)
    name_en: typing.Optional[str] = strawberry.field(description="The English name of the medal type", default=None)
    medalTypeGroup_id: typing.Optional[IDType] = strawberry.field(description="The ID of the medal type group", default=None)


@strawberry.input(description="Attributes needed to delete a medal type")
class MedalTypeDeleteGQLModel:
    id: IDType = strawberry.field(description="The primary key of the medal type")
    lastchange: datetime.datetime = strawberry.field(description="Timestamp for optimistic locking")


@strawberry.mutation(
    description="Creates a new medal type",
    permission_classes=[
        OnlyForAuthentized,
        SimpleInsertPermission[MedalTypeGQLModel](roles=["administrátor"]),
    ]
)
async def medal_type_insert(
    self, info: strawberry.types.Info, medal_type: MedalTypeInsertGQLModel
) -> typing.Union[MedalTypeGQLModel, InsertError[MedalTypeGQLModel]]:
    return await Insert[MedalTypeGQLModel].DoItSafeWay(info=info, entity=medal_type)


@strawberry.mutation(
    description="Updates an existing medal type",
    permission_classes=[
        OnlyForAuthentized,
        SimpleUpdatePermission[MedalTypeGQLModel](roles=["administrátor"]),
    ]
)
async def medal_type_update(
    self, info: strawberry.types.Info, medal_type: MedalTypeUpdateGQLModel
) -> typing.Union[MedalTypeGQLModel, UpdateError[MedalTypeGQLModel]]:
    return await Update[MedalTypeGQLModel].DoItSafeWay(info=info, entity=medal_type)


@strawberry.mutation(
    description="Deletes a medal type",
    permission_classes=[
        OnlyForAuthentized,
        SimpleDeletePermission[MedalTypeGQLModel](roles=["administrátor"]),
    ]
)
async def medal_type_delete(
    self, info: strawberry.types.Info, medal_type: MedalTypeDeleteGQLModel
) -> typing.Optional[DeleteError[MedalTypeGQLModel]]:
    return await Delete[MedalTypeGQLModel].DoItSafeWay(info=info, entity=medal_type)
