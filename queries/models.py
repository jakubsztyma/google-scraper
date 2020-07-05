from django.conf import settings
from django.core import validators as validators
from django.db import models
from django.utils import timezone

from queries import utils


class QueryResultManager(models.Manager):
    def get_or_create(self, user_ip: str, phrase: str):
        phrase = utils.normalize_phrase(phrase)
        result = self.filter(
            user_ip=user_ip,
            phrase=phrase,
            created_at__gt=timezone.now() - settings.QUERY_RESULT_LIFE_TIME
        ).first()

        if result is None:
            response = utils.get_response_from_google(phrase)

            result = self.create(user_ip=user_ip, phrase=phrase, result_count=response.result_count)
            Link.objects.bulk_create(
                Link(query_result=result, url=url, position=position)
                for position, url in enumerate(response.urls)
            )
            PopularWord.objects.bulk_create(
                PopularWord(query_result=result, word=word, position=position)
                for word, position in response.popular_words
            )
        return result


class QueryResult(models.Model):
    user_ip = models.CharField(max_length=15, validators=[validators.validate_ipv4_address])
    phrase = models.CharField(max_length=1000, null=False)
    result_count = models.PositiveIntegerField()
    created_at = models.DateTimeField(editable=False, default=lambda: timezone.now())

    objects = QueryResultManager()


class Link(models.Model):
    query_result = models.ForeignKey(QueryResult, on_delete=models.CASCADE)
    url = models.CharField(max_length=1000, validators=[validators.URLValidator])
    position = models.PositiveIntegerField()


class PopularWord(models.Model):
    query_result = models.ForeignKey(QueryResult, on_delete=models.CASCADE)
    word = models.CharField(max_length=100)
    position = models.PositiveIntegerField()
