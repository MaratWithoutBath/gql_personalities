import strawberry
import typing
from datetime import datetime
from uuid import UUID
from uoishelpers.gqlpermissions import OnlyForAuthentized, SimpleInsertPermission, SimpleUpdatePermission, SimpleDeletePermission
from uoishelpers.resolvers import Insert, InsertError, Update, UpdateError, Delete, DeleteError
from .BaseGQLModel import BaseGQLModel, IDType  # Opravený import pro správné ID
from uoishelpers.resolvers import getLoadersFromInfo  # Pro databázové načítání¨

from .StudyGQLModel import StudyGQLModel, StudyInsertGQLModel, StudyUpdateGQLModel, StudyDeleteGQLModel




@strawberry.type
class StudyGQLModel:
    id: UUID = strawberry.field(description="Primary key: UUID")
    name: str = strawberry.field(description="Name of the study")
    name_en: str = strawberry.field(description="English name of the study")
    program: str = strawberry.field(description="Program of the study")
    start: datetime = strawberry.field(description="Start date and time of the study")
    end: datetime = strawberry.field(description="End date and time of the study")
    user_id: typing.Optional[UUID] = strawberry.field(description="ID of the user associated with this study")

@strawberry.input(description="initial attributes for study insert")
class StudyInsertGQLModel:
    name: str = strawberry.field(description="Name of the study")
    name_en: str = strawberry.field(description="English name of the study")
    program: str = strawberry.field(description="Program of the study")
    start: datetime = strawberry.field(description="Start date and time of the study")
    end: datetime = strawberry.field(description="End date and time of the study")
    user_id: typing.Optional[UUID] = strawberry.field(description="ID of the user associated with this study", default=None)

@strawberry.input(description="set of updateable attributes")
class StudyUpdateGQLModel:
    id: UUID = strawberry.field(description="Primary key")
    lastchange: datetime = strawberry.field(description="Timestamp")

    name: typing.Optional[str] = strawberry.field(description="Name of the study", default=None)
    name_en: typing.Optional[str] = strawberry.field(description="English name of the study", default=None)
    program: typing.Optional[str] = strawberry.field(description="Program of the study", default=None)
    start: typing.Optional[datetime] = strawberry.field(description="Start date and time of the study", default=None)
    end: typing.Optional[datetime] = strawberry.field(description="End date and time of the study", default=None)
    user_id: typing.Optional[UUID] = strawberry.field(description="ID of the user associated with this study", default=None)

@strawberry.input(description="attributes needed for study deletion")
class StudyDeleteGQLModel:
    id: UUID = strawberry.field(description="Primary key")
    lastchange: datetime = strawberry.field(description="Timestamp")


# 🔹 Mutace pro vytvoření (CREATE)
@strawberry.mutation(
    description="Creates a new study",
    permission_classes=[OnlyForAuthentized, SimpleInsertPermission[StudyGQLModel](roles=["administrátor"])]
)
async def study_insert(
    self, info: strawberry.types.Info, entity: StudyInsertGQLModel
) -> typing.Union[StudyGQLModel, InsertError[StudyGQLModel]]:
    return await Insert[StudyGQLModel].DoItSafeWay(info=info, entity=entity)

# 🔹 Mutace pro aktualizaci (UPDATE)
@strawberry.mutation(
    description="Updates an existing study",
    permission_classes=[OnlyForAuthentized, SimpleUpdatePermission[StudyGQLModel](roles=["administrátor"])]
)
async def study_update(
    self, info: strawberry.types.Info, entity: StudyUpdateGQLModel
) -> typing.Union[StudyGQLModel, UpdateError[StudyGQLModel]]:
    return await Update[StudyGQLModel].DoItSafeWay(info=info, entity=entity)

# 🔹 Mutace pro smazání (DELETE)
@strawberry.mutation(
    description="Deletes an existing study",
    permission_classes=[OnlyForAuthentized, SimpleDeletePermission[StudyGQLModel](roles=["administrátor"])]
)
async def study_delete(
    self, info: strawberry.types.Info, entity: StudyDeleteGQLModel
) -> typing.Optional[DeleteError[StudyGQLModel]]:
    return await Delete[StudyGQLModel].DoItSafeWay(info=info, entity=entity)








