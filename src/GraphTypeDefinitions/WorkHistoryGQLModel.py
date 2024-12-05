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
    keys=["id"], description="Entity representing a record of a user's work history"
)
class WorkHistoryGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).WorkHistoryModel

    startdate: typing.Optional[datetime.datetime] = strawberry.field(
        default=None,
        description="The start date of the work period",
        permission_classes=[OnlyForAuthentized]
    )
    enddate: typing.Optional[datetime.datetime] = strawberry.field(
        default=None,
        description="The end date of the work period",
        permission_classes=[OnlyForAuthentized]
    )
    name: typing.Optional[str] = strawberry.field(
        default=None,
        description="Name of the workplace or organization",
        permission_classes=[OnlyForAuthentized]
    )
    ico: typing.Optional[str] = strawberry.field(
        default=None,
        description="Organization ICO (Identification Code)",
        permission_classes=[OnlyForAuthentized]
    )
    user_id: typing.Optional[IDType] = strawberry.field(
        default=None,
        description="The ID of the user associated with this work history",
        permission_classes=[OnlyForAuthentized]
    )
    user: typing.Optional[UserGQLModel] = strawberry.field(
        description="The user associated with this work history",
        permission_classes=[OnlyForAuthentized],
        resolver=ScalarResolver[UserGQLModel](fkey_field_name="user_id")
    )

@createInputs
@dataclasses.dataclass
class WorkHistoryInputFilter:
    startdate: typing.Optional[datetime.datetime] = None
    enddate: typing.Optional[datetime.datetime] = None
    name: typing.Optional[str] = None
    ico: typing.Optional[str] = None
    user_id: typing.Optional[IDType] = None


work_history_by_id = strawberry.field(
    description="Find a work history record by its ID",
    permission_classes=[OnlyForAuthentized],
    graphql_type=typing.Optional[WorkHistoryGQLModel],
    resolver=WorkHistoryGQLModel.load_with_loader
)

work_history_page = strawberry.field(
    description="Fetch paginated work history records",
    permission_classes=[OnlyForAuthentized],
    resolver=PageResolver[WorkHistoryGQLModel](whereType=WorkHistoryInputFilter)
)

@strawberry.input(description="Attributes for creating a work history record")
class WorkHistoryInsertGQLModel:
    startdate: typing.Optional[datetime.datetime] = strawberry.field(description="The start date of the work period", default=None)
    enddate: typing.Optional[datetime.datetime] = strawberry.field(description="The end date of the work period", default=None)
    name: typing.Optional[str] = strawberry.field(description="Name of the workplace or organization", default=None)
    ico: typing.Optional[str] = strawberry.field(description="Organization ICO (Identification Code)", default=None)
    user_id: typing.Optional[IDType] = strawberry.field(description="The ID of the user associated with this work history", default=None)
    id: typing.Optional[IDType] = strawberry.field(description="Primary key (UUID), can be client-generated", default=None)


@strawberry.input(description="Attributes for updating a work history record")
class WorkHistoryUpdateGQLModel:
    id: IDType = strawberry.field(description="The primary key of the work history record")
    lastchange: datetime.datetime = strawberry.field(description="Timestamp for optimistic locking")

    startdate: typing.Optional[datetime.datetime] = strawberry.field(description="The start date of the work period", default=None)
    enddate: typing.Optional[datetime.datetime] = strawberry.field(description="The end date of the work period", default=None)
    name: typing.Optional[str] = strawberry.field(description="Name of the workplace or organization", default=None)
    ico: typing.Optional[str] = strawberry.field(description="Organization ICO (Identification Code)", default=None)
    user_id: typing.Optional[IDType] = strawberry.field(description="The ID of the user associated with this work history", default=None)


@strawberry.input(description="Attributes needed to delete a work history record")
class WorkHistoryDeleteGQLModel:
    id: IDType = strawberry.field(description="The primary key of the work history record")
    lastchange: datetime.datetime = strawberry.field(description="Timestamp for optimistic locking")

@strawberry.mutation(
    description="Creates a new work history record",
    permission_classes=[
        OnlyForAuthentized,
        SimpleInsertPermission[WorkHistoryGQLModel](roles=["administrator"]),
    ]
)
async def work_history_insert(
    self, info: strawberry.types.Info, work_history: WorkHistoryInsertGQLModel
) -> typing.Union[WorkHistoryGQLModel, InsertError[WorkHistoryGQLModel]]:
    return await Insert[WorkHistoryGQLModel].DoItSafeWay(info=info, entity=work_history)


@strawberry.mutation(
    description="Updates an existing work history record",
    permission_classes=[
        OnlyForAuthentized,
        SimpleUpdatePermission[WorkHistoryGQLModel](roles=["administrator"]),
    ]
)
async def work_history_update(
    self, info: strawberry.types.Info, work_history: WorkHistoryUpdateGQLModel
) -> typing.Union[WorkHistoryGQLModel, UpdateError[WorkHistoryGQLModel]]:
    return await Update[WorkHistoryGQLModel].DoItSafeWay(info=info, entity=work_history)


@strawberry.mutation(
    description="Deletes a work history record",
    permission_classes=[
        OnlyForAuthentized,
        SimpleDeletePermission[WorkHistoryGQLModel](roles=["administrator"]),
    ]
)
async def work_history_delete(
    self, info: strawberry.types.Info, work_history: WorkHistoryDeleteGQLModel
) -> typing.Optional[DeleteError[WorkHistoryGQLModel]]:
    return await Delete[WorkHistoryGQLModel].DoItSafeWay(info=info, entity=work_history)
