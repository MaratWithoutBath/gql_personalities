from ast import Call
from typing import Coroutine, Callable, Awaitable, Union, List, Type, Optional
import uuid
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from uoishelpers.resolvers import (
    create1NGetter,
    createEntityByIdGetter,
    createEntityGetter,
    createInsertResolver,
    createUpdateResolver
)
from uoishelpers.resolvers import putSingleEntityToDb

## Nasleduji funkce, ktere lze pouzit jako asynchronni resolvery

###########################################################################################################################
#
# zde si naimportujte sve SQLAlchemy modely
#
###########################################################################################################################

from gql_personalities.DBDefinitions import (
    BaseModel,
    RankModel,
    StudyModel,
    CertificateModel,
    MedalModel,
    WorkHistoryModel,
    RelatedDocModel,
)
from gql_personalities.DBDefinitions import RankTypeModel, CertificateTypeModel, MedalTypeModel
from gql_personalities.DBDefinitions import CertificateCategoryModel, MedalTypeGroupModel


###########################################################################################################################
#
# zde definujte sve resolvery s pomoci funkci vyse
# tyto pouzijete v GraphTypeDefinitions
#
###########################################################################################################################

# user resolvers
# Resolver pro získání hodností uživatele
resolveRanksForUser = create1NGetter(
    RankModel, foreignKeyName="user_id", options=joinedload(RankModel.rankType)
)
# Resolver pro získání studií uživatele
resolveStudiesForUser = create1NGetter(StudyModel, foreignKeyName="user_id")
# Resolver pro získání certifikátů uživatele
resolveCertificatesForUser = create1NGetter(
    CertificateModel,
    foreignKeyName="user_id",
    options=joinedload(CertificateModel.certificateType),
)
# Resolver pro získání medailí uživatele
resolveMedalsForUser = create1NGetter(
    MedalModel, foreignKeyName="user_id", options=joinedload(MedalModel.medalType)
)
# Resolver pro získání pracovních historií uživatele
resolveWorkHistoriesForUser = create1NGetter(WorkHistoryModel, foreignKeyName="user_id")
# Resolver pro získání souvisejících dokumentů uživatele
resolveRelatedDocsForUser = create1NGetter(RelatedDocModel, foreignKeyName="user_id")

# rank resolvers
# Resolver pro získání hodnosti podle ID
resolveRankById = createEntityByIdGetter(RankModel)
# Resolver pro získání všech hodností
resolveRankAll = createEntityGetter(RankModel)
# Resolver pro aktualizaci hodnosti
resolverUpdateRank = createUpdateResolver(RankModel)
# Resolver pro vložení nové hodnosti
resolveInsertRank = createInsertResolver(RankModel)

# rankType resolvers
# Resolver pro získání typu hodnosti podle ID
resolveRankTypeById = createEntityByIdGetter(RankTypeModel)
# Resolver pro získání všech typů hodností
resolveRankTypeAll = createEntityGetter(RankTypeModel)
# Resolver pro aktualizaci typu hodnosti
resolverUpdateRankType = createUpdateResolver(RankTypeModel)
# Resolver pro vložení nového typu hodnosti
resolveInsertRankType = createInsertResolver(RankTypeModel)

async def resolveRankTypeByThreeLetters(
    session: AsyncSession, validity=None, letters: str = ""
) -> List[RankModel]:
    # Resolver pro nalezení typu hodnosti podle tří písmen
    if len(letters) < 3:
        return []
    stmt = select(RankTypeModel).where(RankTypeModel.name.like(f"%{letters}%"))
    if validity is not None:
        stmt = stmt.filter_by(valid=True)

    dbSet = await session.execute(stmt)
    return dbSet.scalars()

# study resolvers
# Resolver pro získání studia podle ID
resolveStudyById = createEntityByIdGetter(StudyModel)
# Resolver pro získání všech studií
resolveStudyAll = createEntityGetter(StudyModel)
# Resolver pro aktualizaci studia
resolverUpdateStudy = createUpdateResolver(StudyModel)
# Resolver pro vložení nového studia
resolveInsertStudy = createInsertResolver(StudyModel)

async def resolveStudyByThreeLetters(
    session: AsyncSession, validity=None, letters: str = ""
) -> List[StudyModel]:
    # Resolver pro nalezení studia podle tří písmen
    if len(letters) < 3:
        return []
    stmt = select(StudyModel).where(
        StudyModel.place.like(f"%{letters}%")
    )  # Study.place. ... kvůli názvu v entitě
    if validity is not None:
        stmt = stmt.filter_by(valid=True)

    dbSet = await session.execute(stmt)
    return dbSet.scalars()

# certificate resolvers
# Resolver pro získání certifikátu podle ID
resolveCertificateById = createEntityByIdGetter(CertificateModel)
# Resolver pro získání všech certifikátů
resolveCertificateAll = createEntityGetter(CertificateModel)
# Resolver pro aktualizaci certifikátu
resolverUpdateCertificate = createUpdateResolver(CertificateModel)
# Resolver pro vložení nového certifikátu
resolveInsertCertificate = createInsertResolver(CertificateModel)

# certificateType resolvers
# Resolver pro získání typu certifikátu podle ID
resolveCertificateTypeById = createEntityByIdGetter(CertificateTypeModel)
# Resolver pro získání všech typů certifikátů
resolveCertificateTypeAll = createEntityGetter(CertificateTypeModel)
# Resolver pro aktualizaci typu certifikátu
resolverUpdateCertificateType = createUpdateResolver(CertificateTypeModel)
# Resolver pro vložení nového typu certifikátu
resolveInsertCertificateType = createInsertResolver(CertificateTypeModel)

async def resolveCertificateTypeByThreeLetters(
    session: AsyncSession, validity=None, letters: str = ""
) -> List[CertificateTypeModel]:
    # Resolver pro nalezení typu certifikátu podle tří písmen
    if len(letters) < 3:
        return []
    stmt = select(CertificateTypeModel).where(CertificateTypeModel.name.like(f"%{letters}%"))
    if validity is not None:
        stmt = stmt.filter_by(valid=True)

    dbSet = await session.execute(stmt)
    return dbSet.scalars()

# certificateTypeGroup resolvers
# Resolver pro získání skupiny typů certifikátů podle ID
resolveCertificateTypeGroupById = createEntityByIdGetter(CertificateCategoryModel)
# Resolver pro získání všech skupin typů certifikátů
resolveCertificateTypeGroupAll = createEntityGetter(CertificateCategoryModel)
# Resolver pro aktualizaci skupiny typů certifikátů
resolverUpdateCertificateTypeGroup = createUpdateResolver(CertificateCategoryModel)
# Resolver pro vložení nové skupiny typů certifikátů
resolveInsertCertificateTypeGroup = createInsertResolver(CertificateCategoryModel)

async def resolveCertificateTypeGroupByThreeLetters(
    session: AsyncSession, validity=None, letters: str = ""
) -> List[CertificateCategoryModel]:
    # Resolver pro nalezení skupiny typů certifikátů podle tří písmen
    if len(letters) < 3:
        return []
    stmt = select(CertificateCategoryModel).where(
        CertificateCategoryModel.name.like(f"%{letters}%")
    )
    if validity is not None:
        stmt = stmt.filter_by(valid=True)

    dbSet = await session.execute(stmt)
    return dbSet.scalars()

# medal resolvers
# Resolver pro získání medaile podle ID
resolveMedalById = createEntityByIdGetter(MedalModel)
# Resolver pro získání všech medailí
resolveMedalAll = createEntityGetter(MedalModel)
# Resolver pro aktualizaci medaile
resolverUpdateMedal = createUpdateResolver(MedalModel)
# Resolver pro vložení nové medaile
resolveInsertMedal = createInsertResolver(MedalModel)

# medalType resolvers
# Resolver pro získání typu medaile podle ID
resolveMedalTypeById = createEntityByIdGetter(MedalTypeModel)
# Resolver pro získání všech typů medailí
resolveMedalTypeAll = createEntityGetter(MedalTypeModel)
# Resolver pro aktualizaci typu medaile
resolverUpdateMedalType = createUpdateResolver(MedalTypeModel)
# Resolver pro vložení nového typu medaile
resolveInsertMedalType = createInsertResolver(MedalTypeModel)

async def resolveMedalTypeByThreeLetters(
    session: AsyncSession, validity=None, letters: str = ""
) -> List[MedalTypeModel]:
    # Resolver pro nalezení typu medaile podle tří písmen
    if len(letters) < 3:
        return []
    stmt = select(MedalTypeModel).where(MedalTypeModel.name.like(f"%{letters}%"))
    if validity is not None:
        stmt = stmt.filter_by(valid=True)

    dbSet = await session.execute(stmt)
    return dbSet.scalars()

# medalTypeGroup resolvers
# Resolver pro získání skupiny typů medailí podle ID
resolveMedalTypeGroupById = createEntityByIdGetter(MedalTypeGroupModel)
# Resolver pro získání všech skupin typů medailí
resolveMedalTypeGroupAll = createEntityGetter(MedalTypeGroupModel)
# Resolver pro aktualizaci skupiny typů medailí
resolverUpdateMedalTypeGroup = createUpdateResolver(MedalTypeGroupModel)
# Resolver pro vložení nové skupiny typů medailí
resolveInsertMedalTypeGroup = createInsertResolver(MedalTypeGroupModel)

async def resolveMedalTypeGroupByThreeLetters(
    session: AsyncSession, validity=None, letters: str = ""
) -> List[MedalTypeGroupModel]:
    # Resolver pro nalezení skupiny typů medailí podle tří písmen
    if len(letters) < 3:
        return []
    stmt = select(MedalTypeGroupModel).where(MedalTypeGroupModel.name.like(f"%{letters}%"))
    if validity is not None:
        stmt = stmt.filter_by(valid=True)

    dbSet = await session.execute(stmt)
    return dbSet.scalars()

# workHistory resolvers
# Resolver pro získání pracovní historie podle ID
resolveWorkHistoryById = createEntityByIdGetter(WorkHistoryModel)
# Resolver pro získání všech pracovních historií
resolveWorkHistoryAll = createEntityGetter(WorkHistoryModel)
# Resolver pro aktualizaci pracovní historie
resolverUpdateWorkHistory = createUpdateResolver(WorkHistoryModel)
# Resolver pro vložení nové pracovní historie
resolveInsertWorkHistory = createInsertResolver(WorkHistoryModel)

async def resolveWorkHistoryByThreeLetters(
    session: AsyncSession, validity=None, letters: str = ""
) -> List[Optional[WorkHistoryModel]]:
    # Resolver pro nalezení pracovní historie podle tří písmen
    if len(letters) < 3:
        return []
    stmt = select(WorkHistoryModel).where(WorkHistoryModel.name.like(f"%{letters}%"))
    if validity is not None:
        stmt = stmt.filter_by(valid=True)

    dbSet = await session.execute(stmt)
    return dbSet.scalars()

# relatedDoc resolvers
# Resolver pro získání souvisejícího dokumentu podle ID
resolveRelatedDocById = createEntityByIdGetter(RelatedDocModel)
# Resolver pro získání všech souvisejících dokumentů
resolveRelatedDocAll = createEntityGetter(RelatedDocModel)
# Resolver pro aktualizaci souvisejícího dokumentu
resolverUpdateRelatedDoc = createUpdateResolver(RelatedDocModel)
# Resolver pro vložení nového souvisejícího dokumentu
resolveInsertRelatedDoc = createInsertResolver(RelatedDocModel)

async def resolveRelatecDocByThreeLetters(
    session: AsyncSession, validity=None, letters: str = ""
) -> List[RelatedDocModel]:
    # Resolver pro nalezení souvisejícího dokumentu podle tří písmen
    if len(letters) < 3:
        return []
    stmt = select(RelatedDocModel).where(RelatedDocModel.name.like(f"%{letters}%"))
    if validity is not None:
        stmt = stmt.filter_by(valid=True)

    dbSet = await session.execute(stmt)
    return dbSet.scalars()
