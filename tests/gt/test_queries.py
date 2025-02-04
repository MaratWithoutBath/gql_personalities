import pytest
import logging
import uuid
import sqlalchemy
import json
import datetime


myquery = """
{
  me {
    id
    fullname
    email
    roles {
      valid
      group { id name }
      roletype { id name }
    }
  }
}"""

@pytest.mark.asyncio
async def test_result_test(NoRole_UG_Server):
    # response = {}
    response = await NoRole_UG_Server(query=myquery, variables={})
    
    print("response", response, flush=True)
    logging.info(f"response {response}")
    pass

from .gt_utils import (
    getQuery,

    createByIdTest2, 
    createUpdateTest2, 
    createTest2, 
    createDeleteTest2
)

test_medal_by_id = createByIdTest2(tableName="medals")
# test_medal_coverage = createByIdTest2(tableName="medals", queryName="coverage")
test_medal_update = createUpdateTest2(tableName="medals", variables={"name": "newname"})
test_medal_create = createTest2(
    tableName="medals", 
    queryName="create", 
    variables={
        "medal_type_id": "cf4c274c-6cf1-11ed-a1eb-0242ac120002",
        "user_id": "e38cba17-4c31-4116-ada7-93abbdab782c",
        "startdate": "2024-12-05T00:00:01"
      })
test_medal_delete = createDeleteTest2(
    tableName="medals", 
    variables={
        "id": "18375c23-767c-4c1e-adb6-9b2beb463533", 
        "medal_type_id": "cf4c274c-6cf1-11ed-a1eb-0242ac120002",
        "user_id": "e38cba17-4c31-4116-ada7-93abbdab782c",
        "startdate": "2024-12-05T00:00:01"
      }
  )

test_medal_type_by_id = createByIdTest2(tableName="medaltypes")
# test_medal_type_page = createTest2(tableName="medaltypes", queryName="readp")
test_medal_type_create = createTest2(
    tableName="medaltypes", 
    queryName="create", 
    variables={
        "name": "newname",
        "medal_category_id": "6299630e-4d27-44a9-a844-53831add33ca"
      })
test_medal_type_update = createUpdateTest2(tableName="medaltypes", variables={"name": "newname"})
test_medal_type_delete = createDeleteTest2(
    tableName="medaltypes", 
    variables={
        "name": "newname",
        "medal_category_id": "6299630e-4d27-44a9-a844-53831add33ca"
    })

test_rank_type_create = createTest2(
    tableName="ranktypes", 
    queryName="create", 
    variables={
            "id": "cf4c274c-6cf1-11ed-a1eb-0242ac120002",
            "name": "newname",
            "nameEn": "newnameEn"
      })

test_study_gql_model_create = createTest2(
    tableName="studies", 
    queryName="create", 
    variables={
        "study_id": "123e4567-e89b-12d3-a456-426614174000",
        "gql_model_id": "987e6543-b21c-34d5-e678-123456789012",
        "startdate": "2024-12-05T00:00:01"
    }
)

test_study_gql_model_update = createUpdateTest2(
    tableName="studies", 
    variables={"startdate": "2025-01-01T00:00:01"}
)

test_study_gql_model_delete = createDeleteTest2(
    tableName="studies", 
    variables={
        "study_id": "123e4567-e89b-12d3-a456-426614174000",
        "gql_model_id": "987e6543-b21c-34d5-e678-123456789012"
    }
)


