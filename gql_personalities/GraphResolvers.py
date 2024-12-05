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
#resolveUserById = createEntityByIdGetter(UserModel)
#resolveUserAll = createEntityGetter(UserModel)

resolveRanksForUser = create1NGetter(
    RankModel, foreignKeyName="user_id", options=joinedload(RankModel.rankType)
)
resolveStudiesForUser = create1NGetter(StudyModel, foreignKeyName="user_id")
resolveCertificatesForUser = create1NGetter(
    CertificateModel,
    foreignKeyName="user_id",
    options=joinedload(CertificateModel.certificateType),
)
resolveMedalsForUser = create1NGetter(
    MedalModel, foreignKeyName="user_id", options=joinedload(MedalModel.medalType)
)
resolveWorkHistoriesForUser = create1NGetter(WorkHistoryModel, foreignKeyName="user_id")
resolveRelatedDocsForUser = create1NGetter(RelatedDocModel, foreignKeyName="user_id")

# rank resolvers
# rank resolvers
resolveRankById = createEntityByIdGetter(RankModel)
resolveRankAll = createEntityGetter(RankModel)
resolverUpdateRank = createUpdateResolver(RankModel)
resolveInsertRank = createInsertResolver(RankModel)
# resolveDeleteRank = createDeleteResolver(RankModel)
# rankType resolvers
# rankType resolvers
resolveRankTypeById = createEntityByIdGetter(RankTypeModel)
resolveRankTypeAll = createEntityGetter(RankTypeModel)
resolverUpdateRankType = createUpdateResolver(RankTypeModel)
resolveInsertRankType = createInsertResolver(RankTypeModel)
# resolveDeleteRankType = createDeleteResolver(RankTypeModel)

async def resolveRankTypeByThreeLetters(
    session: AsyncSession, validity=None, letters: str = ""
) -> List[RankModel]:
    if len(letters) < 3:
        return []
    stmt = select(RankTypeModel).where(RankTypeModel.name.like(f"%{letters}%"))
    if validity is not None:
        stmt = stmt.filter_by(valid=True)

    dbSet = await session.execute(stmt)
    return dbSet.scalars()


# study resolvers
# study resolvers
resolveStudyById = createEntityByIdGetter(StudyModel)
resolveStudyAll = createEntityGetter(StudyModel)
resolverUpdateStudy = createUpdateResolver(StudyModel)
resolveInsertStudy = createInsertResolver(StudyModel)
# resolveDeleteStudy = createDeleteResolver(StudyModel)

async def resolveStudyByThreeLetters(
    session: AsyncSession, validity=None, letters: str = ""
) -> List[StudyModel]:
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
# certificate resolvers
resolveCertificateById = createEntityByIdGetter(CertificateModel)
resolveCertificateAll = createEntityGetter(CertificateModel)
resolverUpdateCertificate = createUpdateResolver(CertificateModel)
resolveInsertCertificate = createInsertResolver(CertificateModel)
# resolveDeleteCertificate = createDeleteResolver(CertificateModel)

# certificateType resolvers
# certificateType resolvers
resolveCertificateTypeById = createEntityByIdGetter(CertificateTypeModel)
resolveCertificateTypeAll = createEntityGetter(CertificateTypeModel)
resolverUpdateCertificateType = createUpdateResolver(CertificateTypeModel)
resolveInsertCertificateType = createInsertResolver(CertificateTypeModel)
# resolveDeleteCertificateType = createDeleteResolver(CertificateTypeModel)

async def resolveCertificateTypeByThreeLetters(
    session: AsyncSession, validity=None, letters: str = ""
) -> List[CertificateTypeModel]:
    if len(letters) < 3:
        return []
    stmt = select(CertificateTypeModel).where(CertificateTypeModel.name.like(f"%{letters}%"))
    if validity is not None:
        stmt = stmt.filter_by(valid=True)

    dbSet = await session.execute(stmt)
    return dbSet.scalars()


# certificateTypeGroup resolvers
resolveCertificateTypeGroupById = createEntityByIdGetter(CertificateCategoryModel)
resolveCertificateTypeGroupAll = createEntityGetter(CertificateCategoryModel)
resolverUpdateCertificateTypeGroup = createUpdateResolver(CertificateCategoryModel)
resolveInsertCertificateTypeGroup = createInsertResolver(CertificateCategoryModel)


async def resolveCertificateTypeGroupByThreeLetters(
    session: AsyncSession, validity=None, letters: str = ""
) -> List[CertificateCategoryModel]:
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
# medal resolvers
resolveMedalById = createEntityByIdGetter(MedalModel)
resolveMedalAll = createEntityGetter(MedalModel)
resolverUpdateMedal = createUpdateResolver(MedalModel)
resolveInsertMedal = createInsertResolver(MedalModel)
# resolveDeleteMedal = createDeleteResolver(MedalModel)

# medalType resolvers
# medalType resolvers
resolveMedalTypeById = createEntityByIdGetter(MedalTypeModel)
resolveMedalTypeAll = createEntityGetter(MedalTypeModel)
resolverUpdateMedalType = createUpdateResolver(MedalTypeModel)
resolveInsertMedalType = createInsertResolver(MedalTypeModel)
# resolveDeleteMedalType = createDeleteResolver(MedalTypeModel)

async def resolveMedalTypeByThreeLetters(
    session: AsyncSession, validity=None, letters: str = ""
) -> List[MedalTypeModel]:
    if len(letters) < 3:
        return []
    stmt = select(MedalTypeModel).where(MedalTypeModel.name.like(f"%{letters}%"))
    if validity is not None:
        stmt = stmt.filter_by(valid=True)

    dbSet = await session.execute(stmt)
    return dbSet.scalars()


# medalTypeGroup resolvers
resolveMedalTypeGroupById = createEntityByIdGetter(MedalTypeGroupModel)
resolveMedalTypeGroupAll = createEntityGetter(MedalTypeGroupModel)
resolverUpdateMedalTypeGroup = createUpdateResolver(MedalTypeGroupModel)
resolveInsertMedalTypeGroup = createInsertResolver(MedalTypeGroupModel)


async def resolveMedalTypeGroupByThreeLetters(
    session: AsyncSession, validity=None, letters: str = ""
) -> List[MedalTypeGroupModel]:
    if len(letters) < 3:
        return []
    stmt = select(MedalTypeGroupModel).where(MedalTypeGroupModel.name.like(f"%{letters}%"))
    if validity is not None:
        stmt = stmt.filter_by(valid=True)

    dbSet = await session.execute(stmt)
    return dbSet.scalars()


# workHistory resolvers
# workHistory resolvers
resolveWorkHistoryById = createEntityByIdGetter(WorkHistoryModel)
resolveWorkHistoryAll = createEntityGetter(WorkHistoryModel)
resolverUpdateWorkHistory = createUpdateResolver(WorkHistoryModel)
resolveInsertWorkHistory = createInsertResolver(WorkHistoryModel)
# resolveDeleteWorkHistory = createDeleteResolver(WorkHistoryModel)

async def resolveWorkHistoryByThreeLetters(
    session: AsyncSession, validity=None, letters: str = ""
) -> List[Optional[WorkHistoryModel]]:
    if len(letters) < 3:
        return []
    stmt = select(WorkHistoryModel).where(WorkHistoryModel.name.like(f"%{letters}%"))
    if validity is not None:
        stmt = stmt.filter_by(valid=True)

    dbSet = await session.execute(stmt)
    return dbSet.scalars()


# relatedDoc resolvers
# relatedDoc resolvers
resolveRelatedDocById = createEntityByIdGetter(RelatedDocModel)
resolveRelatedDocAll = createEntityGetter(RelatedDocModel)
resolverUpdateRelatedDoc = createUpdateResolver(RelatedDocModel)
resolveInsertRelatedDoc = createInsertResolver(RelatedDocModel)
# resolveDeleteRelatedDoc = createDeleteResolver(RelatedDocModel)

async def resolveRelatecDocByThreeLetters(
    session: AsyncSession, validity=None, letters: str = ""
) -> List[RelatedDocModel]:
    if len(letters) < 3:
        return []
    stmt = select(RelatedDocModel).where(RelatedDocModel.name.like(f"%{letters}%"))
    if validity is not None:
        stmt = stmt.filter_by(valid=True)

    dbSet = await session.execute(stmt)
    return dbSet.scalars()
