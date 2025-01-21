import strawberry
from .BaseGQLModel import IDType
from .BaseGQLModel import resolve_reference, BaseGQLModel

@strawberry.federation.type(extend=True, keys=["id"])
class GroupGQLModel(BaseGQLModel):
    id: IDType = strawberry.federation.field(external=True)
