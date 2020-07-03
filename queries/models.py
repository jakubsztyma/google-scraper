from django.core import validators as validators
from django.db import models


class QueryResult(models.Model):
    user_ip = models.CharField(max_length=15, validators=[validators.validate_ipv4_address])
    phrase = models.CharField(max_length=1000, null=False)
    result_count = models.PositiveIntegerField()
    created_at = models.DateTimeField(editable=False, auto_now_add=True)


class Link(models.Model):
    query_result = models.ForeignKey(QueryResult, on_delete=models.CASCADE)
    url = models.CharField(max_length=1000, validators=[validators.URLValidator])
    position = models.PositiveIntegerField()


class PopularWord(models.Model):
    query_result = models.ForeignKey(QueryResult, on_delete=models.CASCADE)
    word = models.CharField(max_length=100)
