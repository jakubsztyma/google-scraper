import random

import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient

from queries.tests import factories


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def get_response_from_google(mocker):
    total_results = random.randint(0, 10e9)
    return mocker.patch('queries.utils._get_response_from_google',
                        return_value={"searchInformation": {"totalResults": str(total_results)}, "items": []})


register(factories.QueryResultFactory)
register(factories.LinkFactory)
