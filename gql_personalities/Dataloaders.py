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

@cache
def composeAuthUrl():
    hostname = os.environ.get("GQLUG_ENDPOINT_URL", None)
    assert hostname is not None, "undefined GQLUG_ENDPOINT_URL"
    assert "://" in hostname, "probably bad formated url, has it 'protocol' part?"
    assert "." not in hostname, "security check failed, change source code"
    return hostname

async def createLoaders_3(asyncSessionMaker):
    pass