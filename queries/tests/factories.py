import factory
from factory import fuzzy

from queries import models


class QueryResultFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.QueryResult

    user_ip = factory.Faker("word")
    phrase = factory.Faker("sentence")
    result_count = fuzzy.FuzzyInteger(0, 1000)


class LinkFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Link

    query_result = factory.SubFactory(QueryResultFactory)
    url = factory.Faker("url")
    position = fuzzy.FuzzyInteger(0, 100)