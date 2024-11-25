import os
import asyncio
import aiohttp
from functools import cache
from aiodataloader import DataLoader
from uoishelpers.dataloaders import createIdLoader, createFkeyLoader

from gql_personalities.DBDefinitions import (
    CertificateModel,
    CertificateTypeModel,
    CertificateTypeGroupModel,
    MedalModel,
    MedalTypeModel,
    MedalTypeGroupModel,
    WorkHistoryModel,
    RelatedDocModel,
    RankModel,
    RankTypeModel,
    StudyModel
)

@cache
def composeAuthUrl(): 
    hostname = os.environ.get("GQLUG_ENDPOINT_URL", None)
    assert hostname is not None, "nedefinovaný GQLUG_ENDPOINT_URL"
    assert "://" in hostname, "pravděpodobně špatně formátovaná URL, obsahuje 'protokol'?"
    assert "." not in hostname, "bezpečnostní kontrola selhala, změňte zdrojový kód"
    return hostname

async def createLoaders_3(asyncSessionMaker):
    class Loaders:
        @property
        @cache
        def certificate_by_id(self):
            return createIdLoader(asyncSessionMaker, CertificateModel)

        @property
        @cache
        def certificate_type_by_id(self):
            return createIdLoader(asyncSessionMaker, CertificateTypeModel)

        @property
        @cache
        def certificate_type_group_by_id(self):
            return createIdLoader(asyncSessionMaker, CertificateTypeGroupModel)

        @property
        @cache
        def medal_by_id(self):
            return createIdLoader(asyncSessionMaker, MedalModel)

        @property
        @cache
        def medal_type_by_id(self):
            return createIdLoader(asyncSessionMaker, MedalTypeModel)

        @property
        @cache
        def medal_type_group_by_id(self):
            return createIdLoader(asyncSessionMaker, MedalTypeGroupModel)

        @property
        @cache
        def work_history_by_id(self):
            return createIdLoader(asyncSessionMaker, WorkHistoryModel)

        @property
        @cache
        def related_doc_by_id(self):
            return createIdLoader(asyncSessionMaker, RelatedDocModel)

        @property
        @cache
        def rank_by_id(self):
            return createIdLoader(asyncSessionMaker, RankModel)

        @property
        @cache
        def rank_type_by_id(self):
            return createIdLoader(asyncSessionMaker, RankTypeModel)

        @property
        @cache
        def study_by_id(self):
            return createIdLoader(asyncSessionMaker, StudyModel)

    return Loaders()

class AuthorizationLoader(DataLoader):

    query = """query($id: UUID!){result: personalityById(id: $id) {roles {user { id } group { id } roletype { id }}}}"""
            # variables = {"id": rbacobject}

    roleUrlEndpoint=None#composeAuthUrl()
    def __init__(self,
        roleUrlEndpoint=roleUrlEndpoint,
        query=query,
        demo=True):
        super().__init__(cache=True)
        self.roleUrlEndpoint = roleUrlEndpoint if roleUrlEndpoint else composeAuthUrl()
        self.query = query
        self.demo = demo
        self.authorizationToken = ""

    def setTokenByInfo(self, info):
        self.authorizationToken = ""

    async def _load(self, id):
        variables = {"id": f"{id}"}
        if self.authorizationToken != "":
            headers = {"authorization": f"Bearer {self.authorizationToken}"}
        else:
            headers = {}
        json = {
            "query": self.query,
            "variables": variables
        }
        roleUrlEndpoint=self.roleUrlEndpoint
        async with aiohttp.ClientSession() as session:
            print(f"query {roleUrlEndpoint} for json={json}")
            async with session.post(url=roleUrlEndpoint, json=json, headers=headers) as resp:
                print(resp.status)
                if resp.status != 200:
                    text = await resp.text()
                    print(text)
                    return []
                else:
                    respJson = await resp.json()

        assert respJson.get("errors", None) is None, respJson["errors"]
        respdata = respJson.get("data", None)
        assert respdata is not None, "missing data response"
        result = respdata.get("result", None)
        assert result is not None, "missing result"
        roles = result.get("roles", None)
        assert roles is not None, "missing roles"
        return [*roles]

    async def batch_load_fn(self, keys):
        reducedkeys = set(keys)
        awaitables = (self._load(key) for key in reducedkeys)
        results = await asyncio.gather(*awaitables)
        indexedResult = {key: result for key, result in zip(reducedkeys, results)}
        results = [indexedResult[key] for key in keys]
        return results