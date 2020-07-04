import json
from collections import Counter

import requests
from django.core import validators as validators
from django.db import models
from django.utils import timezone

from google_scraper import settings


class QueryResultManager(models.Manager):
    def get_or_create(self, user_ip: str, phrase: str):
        now = timezone.now()
        result = self.filter(
            user_ip=user_ip,
            phrase=phrase,
            created_at__gt=now - settings.QUERY_RESULT_LIFE_TIME
        ).first()

        if result is None:
            response = requests.get(settings.SEARCH_URL.format(settings.GOOGLE_KEY, phrase))
            json_result = json.loads(response.content)
            result_count = int(json_result['searchInformation']['totalResults'])
            urls = [item['link'] for item in json_result['items']]
            text = ' '.join(item['title'] for item in json_result['items'])
            popular_words = Counter(text.split()).most_common(10)

            result = self.create(user_ip=user_ip, phrase=phrase, result_count=result_count)
            for position, url in enumerate(urls):
                Link.objects.create(query_result=result, url=url, position=position)
            for word, position in popular_words:
                PopularWord.objects.create(query_result=result, word=word, position=position)
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
