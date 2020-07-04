import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient

from queries.tests import factories


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def get_request(mocker):
    return mocker.patch('requests.get')


register(factories.QueryResultFactory)
register(factories.LinkFactory)
