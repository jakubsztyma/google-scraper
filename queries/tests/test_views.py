from unittest.mock import ANY

from rest_framework import status


class TestIndex:
    def test_get(self, api_client):
        result = api_client.get("/queries/")

        assert result.status_code == status.HTTP_200_OK

    def test_post(self, api_client, mocker):
        phrase = "phrase"
        get_or_create = mocker.patch('queries.models.QueryResultManager.get_or_create')

        result = api_client.post("/queries/", {"phrase": phrase})

        assert result.status_code == status.HTTP_200_OK
        assert get_or_create.called