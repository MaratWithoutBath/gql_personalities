from typing import List, Union
import typing
import strawberry as strawberryA
import uuid
from contextlib import asynccontextmanager
import datetime


@asynccontextmanager
async def withInfo(info):
    # Kontextový manažer pro získání asynchronní session z info
    asyncSessionMaker = info.context["asyncSessionMaker"]
    async with asyncSessionMaker() as session:
        try:
            yield session
        finally:
            pass


def AsyncSessionFromInfo(info):
    # Zastaralá funkce pro získání asynchronní session z info
    print(
        "obsolete function used AsyncSessionFromInfo, use withInfo context manager instead"
    )
    return info.context["session"]


###########################################################################################################################
#
# zde definujte sve GQL modely
# - nove, kde mate zodpovednost
# - rozsirene, ktere existuji nekde jinde a vy jim pridavate dalsi atributy
#
###########################################################################################################################

from gql_personalities.GraphResolvers import (
    resolveRanksForUser,
    resolveStudiesForUser,
    resolveMedalsForUser,
    resolveWorkHistoriesForUser,
    resolveRelatedDocsForUser,
)


@strawberryA.federation.type(extend=True, keys=["id"], permission_classes=[OnlyForAuthentized])
class UserGQLModel:
    # GraphQL model pro uživatele
    id: strawberryA.ID = strawberryA.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: strawberryA.ID):
        return UserGQLModel(id=id)

    @strawberryA.field(description="""List of ranks for the user""", permission_classes=[OnlyForAuthentized])
    async def ranks(self, info: strawberryA.types.Info) -> typing.List["RankGQLModel"]:
        # Resolver pro získání seznamu hodností uživatele
        async with withInfo(info) as session:
            result = await resolveRanksForUser(session, self.id)
            return result

    @strawberryA.field(description="""List of studies for the user""", permission_classes=[OnlyForAuthentized])
    async def studies(
        self, info: strawberryA.types.Info
    ) -> typing.List["StudyGQLModel"]:
        # Resolver pro získání seznamu studií uživatele
        async with withInfo(info) as session:
            result = await resolveStudiesForUser(session, self.id)
            return result

    @strawberryA.field(description="""List of medals for the user""", permission_classes=[OnlyForAuthentized])
    async def medals(
        self, info: strawberryA.types.Info
    ) -> typing.List["MedalGQLModel"]:
        # Resolver pro získání seznamu medailí uživatele
        async with withInfo(info) as session:
            result = await resolveMedalsForUser(session, self.id)
            return result

    @strawberryA.field(description="""List of workHistories for the user""", permission_classes=[OnlyForAuthentized])
    async def work_histories(
        self, info: strawberryA.types.Info
    ) -> typing.List["WorkHistoryGQLModel"]:
        # Resolver pro získání seznamu pracovních historií uživatele
        async with withInfo(info) as session:
            result = await resolveWorkHistoriesForUser(session, self.id)
            return result

    @strawberryA.field(description="""List of relatedDocs for the user""", permission_classes=[OnlyForAuthentized])
    async def related_docs(
        self, info: strawberryA.types.Info
    ) -> typing.List["RelatedDocGQLModel"]:
        # Resolver pro získání seznamu souvisejících dokumentů uživatele
        async with withInfo(info) as session:
            result = await resolveRelatedDocsForUser(session, self.id)
            return result


from gql_personalities.GraphResolvers import resolveRankAll, resolveRankById

@strawberryA.input(description="Model pro vkládání nové hodnosti", permission_classes=[OnlyForAuthentized])
class RankInsertGQLModel:
    # Model pro vkládání hodností
    id: strawberryA.ID
    start: datetime.datetime
    end: datetime.datetime
    rankType_id: strawberryA.ID

@strawberryA.input(description="Model pro aktualizaci existující hodnosti", permission_classes=[OnlyForAuthentized])
class RankUpdateGQLModel:
    # Model pro aktualizaci hodností
    id: strawberryA.ID
    start: datetime.datetime
    end: datetime.datetime
    rankType_id: strawberryA.ID


@strawberryA.federation.type(keys=["id"], description="""Entity representing a rank""", permission_classes=[OnlyForAuthentized])
class RankGQLModel:
    # GraphQL model pro hodnost
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveRankById(session, id)
            result._type_definition = cls._type_definition  # little hack :)
            return result

    @strawberryA.field(description="""primary key""", permission_classes=[OnlyForAuthentized])
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""start""", permission_classes=[OnlyForAuthentized])
    def start(self) -> strawberryA.ID:
        return self.start

    @strawberryA.field(description="""end""", permission_classes=[OnlyForAuthentized])
    def end(self) -> strawberryA.ID:
        return self.end

    # TODO RankTypeGQLModel


from gql_personalities.GraphResolvers import resolveRankTypeAll, resolveRankTypeById
from gql_personalities.GraphResolvers import resolveRankTypeByThreeLetters


@strawberryA.federation.type(
    keys=["id"], description="""Entity representing a rankType""", permission_classes=[OnlyForAuthentized]
)
class RankTypeGQLModel:
    # GraphQL model pro typ hodnosti
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveRankTypeById(session, id)
            result._type_definition = cls._type_definition  # little hack :)
            return result

    @strawberryA.field(description="""primary key""", permission_classes=[OnlyForAuthentized])
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""name""", permission_classes=[OnlyForAuthentized])
    def name(self) -> strawberryA.ID:
        return self.name

    # TODO Ranks Relation


from gql_personalities.GraphResolvers import resolveStudyAll, resolveStudyById
from gql_personalities.GraphResolvers import resolveStudyByThreeLetters


@strawberryA.federation.type(keys=["id"], description="""Entity representing a study""", permission_classes=[OnlyForAuthentized])
class StudyGQLModel:
    # GraphQL model pro studium
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveStudyById(session, id)
            result._type_definition = cls._type_definition  # little hack :)
            return result

    @strawberryA.field(description="""primary key""", permission_classes=[OnlyForAuthentized])
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""place""", permission_classes=[OnlyForAuthentized])
    def place(self) -> strawberryA.ID:
        return self.place

    @strawberryA.field(description="""program""", permission_classes=[OnlyForAuthentized])
    def program(self) -> strawberryA.ID:
        return self.program

    @strawberryA.field(description="""start""", permission_classes=[OnlyForAuthentized])
    def start(self) -> strawberryA.ID:
        return self.start

    @strawberryA.field(description="""end""", permission_classes=[OnlyForAuthentized])
    def end(self) -> strawberryA.ID:
        return self.end


from gql_personalities.GraphResolvers import (
    resolveCertificateAll,
    resolveCertificateById,
)


@strawberryA.federation.type(
    keys=["id"], description="""Entity representing a certificate""", permission_classes=[OnlyForAuthentized]
)
class CertificateGQLModel:
    # GraphQL model pro certifikát
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveCertificateById(session, id)
            result._type_definition = cls._type_definition  # little hack :)
            return result

    @strawberryA.field(description="""primary key""", permission_classes=[OnlyForAuthentized])
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""level""", permission_classes=[OnlyForAuthentized])
    def level(self) -> strawberryA.ID:
        return self.level

    @strawberryA.field(description="""validity start""", permission_classes=[OnlyForAuthentized])
    def validity_start(self) -> strawberryA.ID:
        return self.validity_start

    @strawberryA.field(description="""validity end""", permission_classes=[OnlyForAuthentized])
    def validity_end(self) -> strawberryA.ID:
        return self.validity_end


from gql_personalities.GraphResolvers import (
    resolveCertificateTypeAll,
    resolveCertificateTypeById,
)
from gql_personalities.GraphResolvers import resolveCertificateTypeByThreeLetters


@strawberryA.federation.type(
    keys=["id"], description="""Entity representing a certificateType""", permission_classes=[OnlyForAuthentized]
)
class CertificateTypeGQLModel:
    # GraphQL model pro typ certifikátu
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveCertificateTypeById(session, id)
            result._type_definition = cls._type_definition  # little hack :)
            return result

    @strawberryA.field(description="""primary key""", permission_classes=[OnlyForAuthentized])
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""name""", permission_classes=[OnlyForAuthentized])
    def name(self) -> strawberryA.ID:
        return self.name

    # TODO Certificate Relation


from gql_personalities.GraphResolvers import (
    resolveCertificateTypeGroupAll,
    resolveCertificateTypeGroupById,
)
from gql_personalities.GraphResolvers import resolveCertificateTypeGroupByThreeLetters


@strawberryA.federation.type(
    keys=["id"], description="""Entity representing a certificateTypeGroup""", permission_classes=[OnlyForAuthentized]
)
class CertificateTypeGroupGQLModel:
    # GraphQL model pro skupinu typů certifikátů
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveCertificateTypeGroupById(session, id)
            result._type_definition = cls._type_definition  # little hack :)
            return result

    @strawberryA.field(description="""primary key""", permission_classes=[OnlyForAuthentized])
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""name""", permission_classes=[OnlyForAuthentized])
    def name(self) -> strawberryA.ID:
        return self.name


from gql_personalities.GraphResolvers import resolveMedalAll, resolveMedalById


@strawberryA.federation.type(keys=["id"], description="""Entity representing a medal""", permission_classes=[OnlyForAuthentized])
class MedalGQLModel:
    # GraphQL model pro medaili
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveMedalById(session, id)
            result._type_definition = cls._type_definition  # little hack :)
            return result

    @strawberryA.field(description="""primary key""", permission_classes=[OnlyForAuthentized])
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""year""", permission_classes=[OnlyForAuthentized])
    def year(self) -> strawberryA.ID:
        return self.year


from gql_personalities.GraphResolvers import resolveMedalTypeAll, resolveMedalTypeById
from gql_personalities.GraphResolvers import resolveMedalTypeByThreeLetters


@strawberryA.federation.type(
    keys=["id"], description="""Entity representing a medalType""", permission_classes=[OnlyForAuthentized]
)
class MedalTypeGQLModel:
    # GraphQL model pro typ medaile
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveMedalTypeById(session, id)
            result._type_definition = cls._type_definition  # little hack :)
            return result

    @strawberryA.field(description="""primary key""", permission_classes=[OnlyForAuthentized])
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""name""", permission_classes=[OnlyForAuthentized])
    def name(self) -> strawberryA.ID:
        return self.name


from gql_personalities.GraphResolvers import (
    resolveMedalTypeGroupAll,
    resolveMedalTypeGroupById,
)
from gql_personalities.GraphResolvers import resolveMedalTypeGroupByThreeLetters


@strawberryA.federation.type(
    keys=["id"], description="""Entity representing a medalTypeGroup""", permission_classes=[OnlyForAuthentized]
)
class MedalTypeGroupGQLModel:
    # GraphQL model pro skupinu typů medailí
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveMedalTypeGroupById(session, id)
            result._type_definition = cls._type_definition  # little hack :)
            return result

    @strawberryA.field(description="""primary key""", permission_classes=[OnlyForAuthentized])
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""name""", permission_classes=[OnlyForAuthentized])
    def name(self) -> strawberryA.ID:
        return self.name


from gql_personalities.GraphResolvers import (
    resolveWorkHistoryAll,
    resolveWorkHistoryById,
)
from gql_personalities.GraphResolvers import resolveWorkHistoryByThreeLetters


@strawberryA.federation.type(
    keys=["id"], description="""Entity representing a workHistory""", permission_classes=[OnlyForAuthentized]
)
class WorkHistoryGQLModel:
    # GraphQL model pro pracovní historii
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveWorkHistoryById(session, id)
            result._type_definition = cls._type_definition  # little hack :)
            return result

    @strawberryA.field(description="""primary key""", permission_classes=[OnlyForAuthentized])
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""start""", permission_classes=[OnlyForAuthentized])
    def start(self) -> strawberryA.ID:
        return self.start

    @strawberryA.field(description="""end""", permission_classes=[OnlyForAuthentized])
    def end(self) -> strawberryA.ID:
        return self.end

    @strawberryA.field(description="""position""", permission_classes=[OnlyForAuthentized])
    def position(self) -> strawberryA.ID:
        return self.position

    @strawberryA.field(description="""ico""", permission_classes=[OnlyForAuthentized])
    def ico(self) -> Union[strawberryA.ID, None]:
        return self.ico


from gql_personalities.GraphResolvers import resolveRelatedDocAll, resolveRelatedDocById


@strawberryA.federation.type(
    keys=["id"], description="""Entity representing a relatedDoc""", permission_classes=[OnlyForAuthentized]
)
class RelatedDocGQLModel:
    # GraphQL model pro související dokument
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveRelatedDocById(session, id)
            result._type_definition = cls._type_definition  # little hack :)
            return result

    @strawberryA.field(description="""primary key""", permission_classes=[OnlyForAuthentized])
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""name""", permission_classes=[OnlyForAuthentized])
    def name(self) -> strawberryA.ID:
        return self.name

    # @strawberryA.field(description="""uploaded""")
    # def uploaded(self) -> strawberryA.ID:
    #    return self.uploaded


###########################################################################################################################
#
# zde definujte svuj Query model
#
###########################################################################################################################


@strawberryA.type(description="""Type for query root""", permission_classes=[OnlyForAuthentized])
class Query:
    # Kořenový typ pro dotazy

    # rank
    @strawberryA.field(description="""Returns a list of ranks (paged)""", permission_classes=[OnlyForAuthentized])
    async def rank_page(
        self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10
    ) -> List[RankGQLModel]:
        # Resolver pro získání seznamu hodností (stránkovaný)
        async with withInfo(info) as session:
            result = await resolveRankAll(session, skip, limit)
            return result

    @strawberryA.field(description="""Finds a Rank by their id""", permission_classes=[OnlyForAuthentized])
    async def rank_by_id(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> Union[RankGQLModel, None]:
        # Resolver pro nalezení hodnosti podle ID
        async with withInfo(info) as session:
            result = await resolveRankById(session, id)
            return result

    # rankTypes
    @strawberryA.field(description="""Returns a list of rankTypes (paged)""", permission_classes=[OnlyForAuthentized])
    async def rankType_page(
        self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10
    ) -> List[RankTypeGQLModel]:
        # Resolver pro získání seznamu typů hodností (stránkovaný)
        async with withInfo(info) as session:
            result = await resolveRankTypeAll(session, skip, limit)
            return result

    @strawberryA.field(
        description="""Finds a rankType by letters, letters should be atleast three""", permission_classes=[OnlyForAuthentized]
    )
    async def rankType_by_letters(
        self,
        info: strawberryA.types.Info,
        validity: Union[bool, None] = None,
        letters: str = "",
    ) -> List[RankTypeGQLModel]:
        # Resolver pro nalezení typu hodnosti podle písmen
        async with withInfo(info) as session:
            result = await resolveRankTypeByThreeLetters(session, validity, letters)
            return result

    # study
    @strawberryA.field(description="""Returns a list of studies (paged)""", permission_classes=[OnlyForAuthentized])
    async def study_page(
        self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10
    ) -> List[StudyGQLModel]:
        # Resolver pro získání seznamu studií (stránkovaný)
        async with withInfo(info) as session:
            result = await resolveStudyAll(session, skip, limit)
            return result

    @strawberryA.field(
        description="""Finds a study by letters, letters should be atleast three""", permission_classes=[OnlyForAuthentized]
    )
    async def study_by_letters(
        self,
        info: strawberryA.types.Info,
        validity: Union[bool, None] = None,
        letters: str = "",
    ) -> List[StudyGQLModel]:
        # Resolver pro nalezení studia podle písmen
        async with withInfo(info) as session:
            result = await resolveStudyByThreeLetters(session, validity, letters)
            return result

    # certificate
    @strawberryA.field(description="""Returns a list of certificates (paged)""", permission_classes=[OnlyForAuthentized])
    async def certificate_page(
        self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10
    ) -> List[CertificateGQLModel]:
        # Resolver pro získání seznamu certifikátů (stránkovaný)
        async with withInfo(info) as session:
            result = await resolveCertificateAll(session, skip, limit)
            return result

    # certificateType
    @strawberryA.field(description="""Returns a list of certificateTypes (paged)""", permission_classes=[OnlyForAuthentized])
    async def certificateType_page(
        self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10
    ) -> List[CertificateTypeGQLModel]:
        # Resolver pro získání seznamu typů certifikátů (stránkovaný)
        async with withInfo(info) as session:
            result = await resolveCertificateTypeAll(session, skip, limit)
            return result

    @strawberryA.field(
        description="""Finds a certificateType by letters, letters should be atleast three""", permission_classes=[OnlyForAuthentized]
    )
    async def certificateType_by_letters(
        self,
        info: strawberryA.types.Info,
        validity: Union[bool, None] = None,
        letters: str = "",
    ) -> List[CertificateTypeGQLModel]:
        # Resolver pro nalezení typu certifikátu podle písmen
        async with withInfo(info) as session:
            result = await resolveCertificateTypeByThreeLetters(
                session, validity, letters
            )
            return result

    # certificateTypeGroup
    @strawberryA.field(
        description="""Returns a list of certificateTypeGroups (paged)""", permission_classes=[OnlyForAuthentized]
    )
    async def certificateTypeGroup_page(
        self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10
    ) -> List[CertificateTypeGroupGQLModel]:
        # Resolver pro získání seznamu skupin typů certifikátů (stránkovaný)
        async with withInfo(info) as session:
            result = await resolveCertificateTypeGroupAll(session, skip, limit)
        return result

    @strawberryA.field(
        description="""Finds a certificateTypeGroup by letters, letters should be atleast three""", permission_classes=[OnlyForAuthentized]
    )
    async def certificateTypeGroup_by_letters(
        self,
        info: strawberryA.types.Info,
        validity: Union[bool, None] = None,
        letters: str = "",
    ) -> List[CertificateTypeGroupGQLModel]:
        # Resolver pro nalezení skupiny typů certifikátů podle písmen
        async with withInfo(info) as session:
            result = await resolveCertificateTypeGroupByThreeLetters(
                session, validity, letters
            )
            return result

    # medal
    @strawberryA.field(description="""Returns a list of medals (paged)""", permission_classes=[OnlyForAuthentized])
    async def medal_page(
        self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10
    ) -> List[MedalGQLModel]:
        # Resolver pro získání seznamu medailí (stránkovaný)
        async with withInfo(info) as session:
            result = await resolveMedalAll(session, skip, limit)
            return result

    # medalType
    @strawberryA.field(description="""Returns a list of medalTypes (paged)""", permission_classes=[OnlyForAuthentized])
    async def medalType_page(
        self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10
    ) -> List[MedalTypeGQLModel]:
        # Resolver pro získání seznamu typů medailí (stránkovaný)
        async with withInfo(info) as session:
            result = await resolveMedalTypeAll(session, skip, limit)
            return result

    @strawberryA.field(
        description="""Finds a medalType by letters, letters should be atleast three""", permission_classes=[OnlyForAuthentized]
    )
    async def medalType_by_letters(
        self,
        info: strawberryA.types.Info,
        validity: Union[bool, None] = None,
        letters: str = "",
    ) -> List[MedalTypeGQLModel]:
        # Resolver pro nalezení typu medaile podle písmen
        async with withInfo(info) as session:
            result = await resolveMedalTypeByThreeLetters(session, validity, letters)
            return result

    # medalTypeGroup
    @strawberryA.field(description="""Returns a list of medalTypeGroups (paged)""", permission_classes=[OnlyForAuthentized])
    async def medalTypeGroup_page(
        self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10
    ) -> List[MedalTypeGroupGQLModel]:
        # Resolver pro získání seznamu skupin typů medailí (stránkovaný)
        async with withInfo(info) as session:
            result = await resolveMedalTypeGroupAll(session, skip, limit)
            return result

    @strawberryA.field(
        description="""Finds a medalTypeGroup by letters, letters should be atleast three""", permission_classes=[OnlyForAuthentized]
    )
    async def medalTypeGroup_by_letters(
        self,
        info: strawberryA.types.Info,
        validity: Union[bool, None] = None,
        letters: str = "",
    ) -> List[MedalTypeGroupGQLModel]:
        # Resolver pro nalezení skupiny typů medailí podle písmen
        async with withInfo(info) as session:
            result = await resolveMedalTypeGroupByThreeLetters(
                session, validity, letters
            )
            return result

    # workHistory
    @strawberryA.field(description="""Returns a list of workHistories (paged)""", permission_classes=[OnlyForAuthentized])
    async def workHistory_page(
        self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10
    ) -> List[WorkHistoryGQLModel]:
        # Resolver pro získání seznamu pracovních historií (stránkovaný)
        async with withInfo(info) as session:
            result = await resolveWorkHistoryAll(session, skip, limit)
            return result

    @strawberryA.field(
        description="""Finds a workHistory by letters, letters should be atleast three""", permission_classes=[OnlyForAuthentized]
    )
    async def workHistory_by_letters(
        self,
        info: strawberryA.types.Info,
        validity: Union[bool, None] = None,
        letters: str = "",
    ) -> List[WorkHistoryGQLModel]:
        # Resolver pro nalezení pracovní historie podle písmen
        async with withInfo(info) as session:
            result = await resolveWorkHistoryByThreeLetters(session, validity, letters)
            return result

    # relatedDoc
    @strawberryA.field(description="""Returns a list of relatedDocs (paged)""", permission_classes=[OnlyForAuthentized])
    async def relatedDoc_page(
        self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10
    ) -> List[RelatedDocGQLModel]:
        # Resolver pro získání seznamu souvisejících dokumentů (stránkovaný)
        async with withInfo(info) as session:
            result = await resolveRelatedDocAll(session, skip, limit)
            return result
        
###########################################################################################################################
#
# Tady tvoř CUD operace
# 
#
###########################################################################################################################
        
from uoishelpers.gqlpermissions import (
    OnlyForAuthentized,
    SimpleInsertPermission, 
    SimpleUpdatePermission, 
    SimpleDeletePermission
)    
from uoishelpers.resolvers import (
    getLoadersFromInfo, 
    createInputs,

    InsertError, 
    Insert, 
    UpdateError, 
    Update, 
    DeleteError, 
    Delete
)


@strawberryA.type(description="""Type for mutation root""", permission_classes=[OnlyForAuthentized])
class Mutation:
    # Kořenový typ pro mutace
    #@strawberryA.field(
    #    description="""Inserts a rank""",
    #    permission_classes=[
    #        OnlyForAuthentized
    #    ])
    #async def rank_insert(
    #    self, info: strawberryA.types.Info, rank: RankInsertGQLModel) -> typing.Union["RankGQLModel", InsertError["RankGQLModel"]]:
    #    return await Insert[RankGQLModel].DoItSafeWay(info=info, entity=rank)

    @strawberryA.field(
        description="""Updates the rank""",
        permission_classes=[
            OnlyForAuthentized
        ])
    async def rank_update(
        self, info: strawberryA.types.Info, rank: RankUpdateGQLModel) -> typing.Union["RankGQLModel", UpdateError["RankGQLModel"]]:
        # Mutace pro aktualizaci hodnosti
        return await Update[RankGQLModel].DoItSafeWay(info=info, entity=rank)

    @strawberryA.field(
        description="""Delete the rank""",
        permission_classes=[
            OnlyForAuthentized
        ]
        )
    async def rank_delete(
        self, info: strawberryA.types.Info, rank: RankUpdateGQLModel) -> typing.Optional[UpdateError["RankGQLModel"]]:
        # Mutace pro smazání hodnosti
        return await Update[RankGQLModel].DoItSafeWay(info=info, entity=rank)


###########################################################################################################################
#
# Schema je pouzito v main.py, vsimnete si parametru types, obsahuje vyjmenovane modely. Bez explicitniho vyjmenovani
# se ve schema objevi jen ty struktury, ktere si strawberry dokaze odvodit z Query. Protoze v teto konkretni implementaci
# nektere modely nejsou s Query propojene je potreba je explicitne vyjmenovat. Jinak ve federativnim schematu nebude
# dostupne rozsireni, ktere tento prvek federace implementuje.
#
###########################################################################################################################
from uoishelpers.schema import WhoAmIExtension

schema = strawberryA.federation.Schema(
    # Definice schématu GraphQL
    query=Query,
    mutation=Mutation,
    types=(UserGQLModel,),
    extensions=[WhoAmIExtension],
)
