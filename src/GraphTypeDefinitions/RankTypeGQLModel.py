import typing
import datetime
import strawberry
import dataclasses
from uoishelpers.gqlpermissions import (
    OnlyForAuthentized,
    SimpleInsertPermission, 
    SimpleUpdatePermission, 
    SimpleDeletePermission
)    
from uoishelpers.resolvers import (
    getLoadersFromInfo, 
    createInputs,

    InsertError, 
    Insert, 
    UpdateError, 
    Update, 
    DeleteError, 
    Delete,

    PageResolver,
    VectorResolver,
    ScalarResolver
)

from .BaseGQLModel import BaseGQLModel, IDType


@strawberry.federation.type(
    keys=["id"], description="""Entity representing a Rank Type"""
)
class RankTypeGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).RankTypeModel

    name: typing.Optional[str] = strawberry.field(
        default=None,
        description="""Name of the rank type""",
        permission_classes=[OnlyForAuthentized]
    )
    
    name_en: typing.Optional[str] = strawberry.field(
        default=None,
        description="""English name of the rank type""",
        permission_classes=[OnlyForAuthentized]
    )

    rank: typing.List["RankGQLModel"] = strawberry.field(
        description="""Ranks associated with this rank type""",
        permission_classes=[OnlyForAuthentized],
        resolver=VectorResolver["RankGQLModel"](fkey_field_name="ranktype_id")
    )

@createInputs
@dataclasses.dataclass
class RankTypeInputFilter:
    name: typing.Optional[str] = strawberry.field(
        description="Filter by rank type name",
        default=None,
        permission_classes=[OnlyForAuthentized]
    )
    name_en: str

rank_type_by_id = strawberry.field(
    description="""Finds a rank type by its ID""",
    permission_classes=[OnlyForAuthentized],
    graphql_type=typing.Optional[RankTypeGQLModel],
    resolver=RankTypeGQLModel.load_with_loader
)

rank_type_page = strawberry.field(
    description="""Finds paged rank types""",
    permission_classes=[OnlyForAuthentized],
    resolver=PageResolver[RankTypeGQLModel](whereType=RankTypeInputFilter)
)

@strawberry.input(description="initial attributes for rank type insert")
class RankTypeInsertGQLModel:
    name: str = strawberry.field(
        description="name of the rank type",
        permission_classes=[OnlyForAuthentized]
    )
    name_en: str = strawberry.field(description="english name of the rank type")

@strawberry.input(description="set of updateable attributes")
class RankTypeUpdateGQLModel:
    id: IDType = strawberry.field(description="primary key", permission_classes=[OnlyForAuthentized])
    lastchange: datetime.datetime = strawberry.field(description="timestamp", permission_classes=[OnlyForAuthentized])

    name: typing.Optional[str] = strawberry.field(
        description="name of the rank type",
        default=None,
        permission_classes=[OnlyForAuthentized]
    )
    name_en: typing.Optional[str] = strawberry.field(
        description="english name of the rank type",
        default=None,
        permission_classes=[OnlyForAuthentized]
    )

@strawberry.input(description="attributes needed for rank type deletion")
class RankTypeDeleteGQLModel:
    id: IDType = strawberry.field(description="primary key", permission_classes=[OnlyForAuthentized])
    lastchange: datetime.datetime = strawberry.field(description="timestamp", permission_classes=[OnlyForAuthentized])

@strawberry.mutation(
    description="Inserts a new rank type",
    permission_classes=[
        OnlyForAuthentized,
        SimpleInsertPermission[RankTypeGQLModel](roles=["admin"])]
)
async def rank_type_insert(self, info: strawberry.types.Info, rank_type: RankTypeInsertGQLModel) -> typing.Union[RankTypeGQLModel, InsertError[RankTypeGQLModel]]:
    return await Insert[RankTypeGQLModel].DoItSafeWay(info=info, entity=rank_type)

@strawberry.mutation(
    description="Updates an existing rank type",
    permission_classes=[
        OnlyForAuthentized,
        SimpleUpdatePermission[RankTypeGQLModel](roles=["admin"])]
)
async def rank_type_update(self, info: strawberry.types.Info, rank_type: typing.Annotated[RankTypeUpdateGQLModel, strawberry.argument(description="desc")]) -> typing.Union[RankTypeGQLModel, UpdateError[RankTypeGQLModel]]:
    return await Update[RankTypeGQLModel].DoItSafeWay(info=info, entity=rank_type)

@strawberry.mutation(
    description="Deletes a rank type",
    permission_classes=[
        OnlyForAuthentized,
        SimpleDeletePermission[RankTypeGQLModel](roles=["admin"])]
)
async def rank_type_delete(self, info: strawberry.types.Info, rank_type: RankTypeDeleteGQLModel) -> typing.Optional[DeleteError[RankTypeGQLModel]]:
    return await Delete[RankTypeGQLModel].DoItSafeWay(info=info, entity=rank_type)
