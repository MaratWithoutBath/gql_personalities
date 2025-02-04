import strawberry

# Import all query fields
from .CertificateGQLModel import certificate_by_id, certificate_page
from .CertificateTypeGQLModel import certificate_type_by_id, certificate_type_page
from .CertificateCategoryGQLModel import certificate_category_by_id, certificate_category_page
from .MedalGQLModel import medal_by_id, medal_page
from .MedalTypeGQLModel import medal_type_by_id, medal_type_page
from .MedalCategoryGQLModel import medal_category_by_id, medal_category_page
from .WorkHistoryGQLModel import work_history_by_id, work_history_page
from .RelatedDocGQLModel import related_doc_by_id, related_doc_page
from .RankGQLModel import rank_by_id, rank_page
from .RankTypeGQLModel import rank_type_by_id, rank_type_page
# from .StudyGQLModel import study_by_id, study_page  # Odstraněn import pro StudyGQLModel

@strawberry.type(description="Root Query for all entities")
class Query:
    # Certificate queries
    certificate_by_id = certificate_by_id
    certificate_page = certificate_page

    # Certificate Type queries
    certificate_type_by_id = certificate_type_by_id
    certificate_type_page = certificate_type_page

    # Certificate Type Group queries
    # certificate_category_by_id = certificate_category_by_id
    # certificate_category_page = certificate_category_page

    # Medal queries
    medal_by_id = medal_by_id
    medal_page = medal_page

    # Medal Type queries
    medal_type_by_id = medal_type_by_id
    medal_type_page = medal_type_page

    # Medal Category queries
    medal_category_by_id = medal_category_by_id
    medal_category_page = medal_category_page

    # Work History queries
    work_history_by_id = work_history_by_id
    work_history_page = work_history_page

    # Related Document queries
    related_doc_by_id = related_doc_by_id
    related_doc_page = related_doc_page

    # Rank queries
    rank_by_id = rank_by_id
    rank_page = rank_page

    # Rank Type queries
    rank_type_by_id = rank_type_by_id
    rank_type_page = rank_type_page

    # Study queries
    # study_by_id = study_by_id
    # study_page = study_page
