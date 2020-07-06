from django.urls import reverse
from rest_framework import status

from queries import views


class TestIndex:
    url = reverse(views.index)

    def test_get(self, api_client):
        result = api_client.get(self.url)

        assert result.status_code == status.HTTP_200_OK

    def test_post(self, api_client, mocker):
        phrase = "phrase"
        get_or_create = mocker.patch('queries.models.QueryResultManager.get_or_create')

        result = api_client.post(self.url, {"phrase": phrase})

        assert result.status_code == status.HTTP_200_OK
        assert get_or_create.called


class TestProxy:
    def test_get(self, api_client, get_response_from_google):
        phrase = 'fake'

        result = api_client.get(reverse(views.proxy, kwargs={'phrase': phrase}))

        assert result.status_code == status.HTTP_200_OK
        get_response_from_google.assert_called_with(phrase)
