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

MedalTypeGQLModel = typing.Annotated["MedalTypeGQLModel", strawberry.lazy(".MedalTypeGQLModel")]

@strawberry.federation.type(
    keys=["id"], description="Entity representing a medal category"
)
class MedalCategoryGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).MedalCategoryModel

    name: typing.Optional[str] = strawberry.field(
        default=None,
        description="The name of the medal category",
        permission_classes=[OnlyForAuthentized]
    )
    name_en: typing.Optional[str] = strawberry.field(
        default=None,
        description="The English name of the medal category",
        permission_classes=[OnlyForAuthentized]
    )

    medalTypes: typing.List[MedalTypeGQLModel] = strawberry.field(
        description="List of medal types belonging to this category",
        permission_classes=[OnlyForAuthentized],
        resolver=VectorResolver[MedalTypeGQLModel](fkey_field_name="medalTypeGroup_id", whereType=None)
    )


@createInputs
@dataclasses.dataclass
class MedalCategoryInputFilter:
    name: typing.Optional[str] = strawberry.field(
        description="Filter by name",
        default=None,
        permission_classes=[OnlyForAuthentized]
    )
    name_en: typing.Optional[str] = strawberry.field(
        description="Filter by English name",
        default=None,
        permission_classes=[OnlyForAuthentized]
    )


medal_category_by_id = strawberry.field(
    description="Find a medal category by its ID",
    permission_classes=[OnlyForAuthentized],
    graphql_type=typing.Optional[MedalCategoryGQLModel],
    resolver=MedalCategoryGQLModel.load_with_loader
)

medal_category_page = strawberry.field(
    description="Fetch paginated medal categories",
    permission_classes=[OnlyForAuthentized],
    resolver=PageResolver[MedalCategoryGQLModel](whereType=MedalCategoryInputFilter)
)


@strawberry.input(description="Attributes for creating a medal category")
class MedalCategoryInsertGQLModel:
    name: str = strawberry.field(description="The name of the medal category")
    name_en: typing.Optional[str] = strawberry.field(description="The English name of the medal category", default=None)
    id: typing.Optional[IDType] = strawberry.field(description="Primary key (UUID), can be client-generated", default=None)


@strawberry.input(description="Attributes for updating a medal category")
class MedalCategoryUpdateGQLModel:
    id: IDType = strawberry.field(description="The primary key of the medal category")
    lastchange: datetime.datetime = strawberry.field(description="Timestamp for optimistic locking")

    name: typing.Optional[str] = strawberry.field(description="The name of the medal category", default=None)
    name_en: typing.Optional[str] = strawberry.field(description="The English name of the medal category", default=None)


@strawberry.input(description="Attributes needed to delete a medal category")
class MedalCategoryDeleteGQLModel:
    id: IDType = strawberry.field(description="The primary key of the medal category")
    lastchange: datetime.datetime = strawberry.field(description="Timestamp for optimistic locking")


@strawberry.mutation(
    description="Creates a new medal category",
    permission_classes=[
        OnlyForAuthentized,
        SimpleInsertPermission[MedalCategoryGQLModel](roles=["administrátor"]),
    ]
)
async def medal_category_insert(
    self, info: strawberry.types.Info, medal_category: MedalCategoryInsertGQLModel
) -> typing.Union[MedalCategoryGQLModel, InsertError[MedalCategoryGQLModel]]:
    return await Insert[MedalCategoryGQLModel].DoItSafeWay(info=info, entity=medal_category)


@strawberry.mutation(
    description="Updates an existing medal category",
    permission_classes=[
        OnlyForAuthentized,
        SimpleUpdatePermission[MedalCategoryGQLModel](roles=["administrátor"]),
    ]
)
async def medal_category_update(
    self, info: strawberry.types.Info, medal_category: MedalCategoryUpdateGQLModel
) -> typing.Union[MedalCategoryGQLModel, UpdateError[MedalCategoryGQLModel]]:
    return await Update[MedalCategoryGQLModel].DoItSafeWay(info=info, entity=medal_category)


@strawberry.mutation(
    description="Deletes a medal category",
    permission_classes=[
        OnlyForAuthentized,
        SimpleDeletePermission[MedalCategoryGQLModel](roles=["administrátor"]),
    ]
)
async def medal_category_delete(
    self, info: strawberry.types.Info, medal_category: MedalCategoryDeleteGQLModel
) -> typing.Optional[DeleteError[MedalCategoryGQLModel]]:
    return await Delete[MedalCategoryGQLModel].DoItSafeWay(info=info, entity=medal_category)
