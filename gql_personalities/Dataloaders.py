import os
import asyncio
import aiohttp
from functools import cache
from aiodataloader import DataLoader
from uoishelpers.dataloaders import createIdLoader, createFkeyLoader

from gql_personalities.DBDefinitions import (
    RankModel,
    RankTypeModel
)

#možná jsem tuhle funkci ukradl od Tomáše Urbana, on mi to ale určitě odpustí 7:)
@cache
def composeAuthUrl(): 
    hostname = os.environ.get("GQLUG_ENDPOINT_URL", None)
    assert hostname is not None, "nedefinovaný GQLUG_ENDPOINT_URL"
    assert "://" in hostname, "pravděpodobně špatně formátovaná URL, obsahuje 'protokol'?"
    assert "." not in hostname, "bezpečnostní kontrola selhala, změňte zdrojový kód"
    return hostname

async def createLoaders_3(asyncSessionMaker):
    pass