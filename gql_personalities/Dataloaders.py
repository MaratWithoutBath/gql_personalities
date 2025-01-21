from uoishelpers.dataloaders import createIdLoader, createFkeyLoader
from functools import cache

from DBDefinitions import BaseModel

def createLoaders(asyncSessionMaker):
    # Vytvoří dataloadery pro všechny modely v BaseModel

    def createLambda(loaderName, DBModel):
        # Lambda funkce pro vytvoření loaderu podle názvu a modelu
        return lambda self: createIdLoader(asyncSessionMaker, DBModel)

    attrs = {}

    for DBModel in BaseModel.registry.mappers:
        # Pro každý model v BaseModel registry vytvoří property s loaderem
        cls = DBModel.class_
        attrs[cls.__tablename__] = property(cache(createLambda(asyncSessionMaker, cls)))
        attrs[cls.__name__] = attrs[cls.__tablename__]
    # attrs["authorizations"] = property(cache(lambda self: AuthorizationLoader()))
    Loaders = type('Loaders', (), attrs)   
    return Loaders()

def createLoadersContext(asyncSessionMaker):
    # Vytvoří kontext s dataloadery
    return {
        "loaders": createLoaders(asyncSessionMaker)
    }