from uoishelpers.dataloaders import createLoadersAuto
from gql_personalities.DBDefinitions import BaseModel

def createLoadersContext(asyncSessionMaker):
    return {
        # "loaders": createLoaders(asyncSessionMaker)
        "loaders": createLoadersAuto(asyncSessionMaker, BaseModel=BaseModel)
    }