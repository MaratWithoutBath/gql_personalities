import strawberry

import strawberry.extensions
from uoishelpers.gqlpermissions import RBACObjectGQLModel
###########################################################################################################################
#
# Schema je pouzito v main.py, vsimnete si parametru types, obsahuje vyjmenovane modely. Bez explicitniho vyjmenovani
# se ve schema objevi jen ty struktury, ktere si strawberry dokaze odvodit z Query. Protoze v teto konkretni implementaci
# nektere modely nejsou s Query propojene je potreba je explicitne vyjmenovat. Jinak ve federativnim schematu nebude
# dostupne rozsireni, ktere tento prvek federace implementuje.
#
###########################################################################################################################

from .UserGQLModel import UserGQLModel
from .GroupGQLModel import GroupGQLModel
from .BaseGQLModel import BaseGQLModel

from .query import Query
from .mutation import Mutation
schema = strawberry.federation.Schema(
    query=Query, 
    mutation=Mutation, 
    types=(UserGQLModel, GroupGQLModel, RBACObjectGQLModel, BaseGQLModel), 
    extensions=[]
)

from uoishelpers.schema import WhoAmIExtension, ProfilingExtension, PrometheusExtension
schema.extensions.append(WhoAmIExtension)
