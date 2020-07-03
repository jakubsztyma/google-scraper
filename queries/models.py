import json
import requests

from django.core import validators as validators
from django.db import models

from google_scraper import settings

SEARCH_URL = "https://www.googleapis.com/customsearch/v1?key={0}&gl=se&cr=se&googlehost=google.se&q={1}&alt=json"


class QueryResultManager(models.Manager):
    def get_or_create(self, user_ip: str, phrase: str):
        result = self.filter(user_ip=user_ip, phrase=phrase).first()
        if result is None:
            response = requests.get(SEARCH_URL.format(settings.GOOGLE_KEY, phrase))
            json_result = json.loads(response.content)
            result_count = json_result['searchInformation']['totalResults']
            urls = [item['link'] for item in json_result['items']]

            result = self.create(user_ip=user_ip, phrase=phrase, result_count=result_count)
            for position, url in enumerate(urls):
                Link.objects.create(query_result=result, url=url, position=position)
        return result


class QueryResult(models.Model):
    user_ip = models.CharField(max_length=15, validators=[validators.validate_ipv4_address])
    phrase = models.CharField(max_length=1000, null=False)
    result_count = models.PositiveIntegerField()
    created_at = models.DateTimeField(editable=False, auto_now_add=True)

    objects = QueryResultManager()


class Link(models.Model):
    query_result = models.ForeignKey(QueryResult, on_delete=models.CASCADE)
    url = models.CharField(max_length=1000, validators=[validators.URLValidator])
    position = models.PositiveIntegerField()


class PopularWord(models.Model):
    query_result = models.ForeignKey(QueryResult, on_delete=models.CASCADE)
    word = models.CharField(max_length=100)
