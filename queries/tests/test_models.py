import pytest

from .. import models

pytestmark = pytest.mark.django_db


class TestQueryResult:
    def test_get_or_create_new_query(self, mocker, get_request):
        user_ip = 'abc'
        phrase = 'abc'
        total_results = 1000
        mocker.patch('json.loads',
                     return_value={"searchInformation": {"totalResults": str(total_results)}, "items": []})

        created = models.QueryResult.objects.get_or_create(user_ip, phrase)

        assert get_request.called
        assert models.QueryResult.objects.count() == 1
        assert created.user_ip == user_ip
        assert created.phrase == phrase
        assert created.result_count == total_results

    def test_get_or_create_query_exists(self, query_result, get_request):
        retrieved = models.QueryResult.objects.get_or_create(query_result.user_ip, query_result.phrase)

        assert not get_request.called
        assert retrieved == query_result
