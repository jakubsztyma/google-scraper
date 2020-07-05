from datetime import timedelta

import pytest
from django.conf import settings
from django.utils import timezone

from .conftest import GOOGLE_SAMPLE_RESPONSE
from .. import models, utils

pytestmark = pytest.mark.django_db


class TestQueryResult:
    def test_get_or_create_new(self, faker, get_response_from_google):
        user_ip = '192,0.0.1'
        phrase = faker.sentence().lower()

        created = models.QueryResult.objects.get_or_create(user_ip, phrase)

        assert get_response_from_google.called
        assert models.QueryResult.objects.count() == 1
        assert created.user_ip == user_ip
        assert created.phrase == phrase
        assert created.link_set.count() == len(GOOGLE_SAMPLE_RESPONSE['items'])
        assert created.popularword_set.count() == 10

    @pytest.mark.freeze_time
    def test_get_or_create_exists_valid(self, query_result_factory, get_response_from_google):
        query_result = query_result_factory(
            created_at=timezone.now() - settings.QUERY_RESULT_LIFE_TIME + timedelta(microseconds=1))
        query_result.phrase = utils.normalize_phrase(query_result.phrase)
        query_result.save()

        retrieved = models.QueryResult.objects.get_or_create(query_result.user_ip, query_result.phrase)

        assert not get_response_from_google.called
        assert retrieved == query_result

    @pytest.mark.freeze_time
    def test_get_or_create_exists_deprecated(self, query_result_factory, get_response_from_google):
        query_result = query_result_factory(created_at=timezone.now() - settings.QUERY_RESULT_LIFE_TIME)

        retrieved = models.QueryResult.objects.get_or_create(query_result.user_ip, query_result.phrase)

        assert get_response_from_google.called
        assert retrieved != query_result
