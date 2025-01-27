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
from .RankTypeGQLModel import RankTypeGQLModel

@strawberry.federation.type(
    keys=["id"], description="""Entity representing a Rank"""
)
class RankGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).RankModel

    start: typing.Optional[datetime.datetime] = strawberry.field(
        default=None,
        description="""Start date of the rank""",
        permission_classes=[OnlyForAuthentized]
    )
    
    end: typing.Optional[datetime.datetime] = strawberry.field(
        default=None,
        description="""End date of the rank""",
        permission_classes=[OnlyForAuthentized]
    )

    user_id: typing.Optional[IDType] = strawberry.field(
        default=None,
        description="""User ID associated with the rank""",
        permission_classes=[OnlyForAuthentized]
    )

    rankType_id: typing.Optional[IDType] = strawberry.field(
        default=None,
        description="""Type ID of the rank""",
        permission_classes=[OnlyForAuthentized]
    )

    rankType: typing.Optional["RankTypeGQLModel"] = strawberry.field(
        description="""Type of the rank""",
        permission_classes=[OnlyForAuthentized],
        resolver=ScalarResolver["RankTypeGQLModel"](fkey_field_name="rankType_id")
    )

@createInputs
@dataclasses.dataclass
class RankInputFilter:
    start: datetime.datetime = strawberry.field(
        description="Filter by start date",
        permission_classes=[OnlyForAuthentized]
    )
    end: datetime.datetime = strawberry.field(
        description="Filter by end date",
        permission_classes=[OnlyForAuthentized]
    )
    user_id: typing.Optional[IDType] = strawberry.field(
        description="Filter by user ID",
        default=None,
        permission_classes=[OnlyForAuthentized]
    )
    ranktype_id: typing.Optional[IDType] = strawberry.field(
        description="Filter by rank type ID",
        default=None,
        permission_classes=[OnlyForAuthentized]
    )

rank_by_id = strawberry.field(
    description="""Finds a rank by its ID""",
    permission_classes=[OnlyForAuthentized],
    graphql_type=typing.Optional[RankGQLModel],
    resolver=RankGQLModel.load_with_loader
)

rank_page = strawberry.field(
    description="""Finds paged ranks""",
    permission_classes=[OnlyForAuthentized],
    resolver=PageResolver[RankGQLModel](whereType=RankInputFilter)
)

@strawberry.input(description="initial attributes for rank insert")
class RankInsertGQLModel:
    start: datetime.datetime = strawberry.field(description="start datetime")
    end: datetime.datetime = strawberry.field(description="end datetime")
    user_id: typing.Optional[IDType] = strawberry.field(description="user ID", default=None)
    ranktype_id: IDType = strawberry.field(description="rank type ID")

@strawberry.input(description="set of updateable attributes")
class RankUpdateGQLModel:
    id: IDType = strawberry.field(description="primary key")
    lastchange: datetime.datetime = strawberry.field(description="timestamp")

    start: typing.Optional[datetime.datetime] = strawberry.field(description="start datetime", default=None)
    end: typing.Optional[datetime.datetime] = strawberry.field(description="end datetime", default=None)
    user_id: typing.Optional[IDType] = strawberry.field(description="user ID", default=None)
    ranktype_id: typing.Optional[IDType] = strawberry.field(description="rank type ID", default=None)

@strawberry.input(description="attributes needed for rank deletion")
class RankDeleteGQLModel:
    id: IDType = strawberry.field(description="primary key")
    lastchange: datetime.datetime = strawberry.field(description="timestamp")

@strawberry.mutation(
    description="Inserts a new rank",
    permission_classes=[
        OnlyForAuthentized,
        SimpleInsertPermission[RankGQLModel](roles=["admin"])
    ]
)
async def rank_insert(self, info: strawberry.types.Info, rank: RankInsertGQLModel) -> typing.Union[RankGQLModel, InsertError[RankGQLModel]]:
    return await Insert[RankGQLModel].DoItSafeWay(info=info, entity=rank)

@strawberry.mutation(
    description="Updates an existing rank",
    permission_classes=[
        OnlyForAuthentized,
        SimpleUpdatePermission[RankGQLModel](roles=["admin"])
    ]
)
async def rank_update(self, info: strawberry.types.Info, rank: typing.Annotated[RankUpdateGQLModel, strawberry.argument(description="desc")]) -> typing.Union[RankGQLModel, UpdateError[RankGQLModel]]:
    return await Update[RankGQLModel].DoItSafeWay(info=info, entity=rank)

@strawberry.mutation(
    description="Deletes a rank",
    permission_classes=[
        OnlyForAuthentized,
        SimpleDeletePermission[RankGQLModel](roles=["admin"])
    ]
)
async def rank_delete(self, info: strawberry.types.Info, rank: RankDeleteGQLModel) -> typing.Optional[DeleteError[RankGQLModel]]:
    return await Delete[RankGQLModel].DoItSafeWay(info=info, entity=rank)
