import strawberry

# Import all mutation fields
from .CertificateGQLModel import certificate_insert, certificate_update, certificate_delete
from .CertificateTypeGQLModel import certificate_type_insert, certificate_type_update, certificate_type_delete
from .CertificateCategoryGQLModel import certificate_type_group_insert, certificate_type_group_update, certificate_type_group_delete
from .MedalGQLModel import medal_insert, medal_update, medal_delete
from .MedalTypeGQLModel import medal_type_insert, medal_type_update, medal_type_delete
from .MedalCategoryGQLModel import medal_category_insert, medal_category_update, medal_category_delete
from .WorkHistoryGQLModel import work_history_insert, work_history_update, work_history_delete
from .RelatedDocGQLModel import related_doc_insert, related_doc_update, related_doc_delete
from .RankTypeGQLModel import rank_type_insert, rank_type_update, rank_type_delete
from .RankGQLModel import rank_insert, rank_update, rank_delete
from .StudyGQLModel import study_insert, study_update, study_delete




@strawberry.type(description="Root Mutation for all entities")
class Mutation:
    # Certificate mutations
    certificate_insert = certificate_insert
    certificate_update = certificate_update
    certificate_delete = certificate_delete

    # Certificate Type mutations
    certificate_type_insert = certificate_type_insert
    certificate_type_update = certificate_type_update
    certificate_type_delete = certificate_type_delete

    # Certificate Type Group mutations
    certificate_type_group_insert = certificate_type_group_insert
    certificate_type_group_update = certificate_type_group_update
    certificate_type_group_delete = certificate_type_group_delete

    # Medal mutations
    medal_insert = medal_insert
    medal_update = medal_update
    medal_delete = medal_delete

    # Medal Type mutations
    medal_type_insert = medal_type_insert
    medal_type_update = medal_type_update
    medal_type_delete = medal_type_delete

    # Medal Category mutations
    medal_category_insert = medal_category_insert
    medal_category_update = medal_category_update
    medal_category_delete = medal_category_delete

    # Work History mutations
    work_history_insert = work_history_insert
    work_history_update = work_history_update
    work_history_delete = work_history_delete

    # Related Document mutations
    related_doc_insert = related_doc_insert
    related_doc_update = related_doc_update
    related_doc_delete = related_doc_delete

    # Rank Type mutations
    rank_type_insert = rank_type_insert
    rank_type_update = rank_type_update
    rank_type_delete = rank_type_delete

    # Rank mutations
    rank_insert = rank_insert
    rank_update = rank_update
    rank_delete = rank_delete

    # Study mutations
    study_insert = study_insert
    study_update = study_update
    study_delete = study_delete

    
