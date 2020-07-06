import random

import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient
from faker import Faker

from queries.tests import factories

faker = Faker()
GOOGLE_SAMPLE_RESPONSE = {
    "searchInformation": {"totalResults": str(random.randint(0, 10e9))},
    "items": [
        {'link': faker.url(), 'title': faker.sentence()}
        for _ in range(20)
    ]
}

@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def get_response_from_google(mocker):
    return mocker.patch('queries.utils.get_response_from_google',
                        return_value=GOOGLE_SAMPLE_RESPONSE)


register(factories.QueryResultFactory)
register(factories.LinkFactory)
