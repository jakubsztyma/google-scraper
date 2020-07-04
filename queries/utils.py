import json
from collections import Counter, Generator
from dataclasses import dataclass

import requests
from django.conf import settings


@dataclass
class GoogleResult:
    result_count: int
    urls: Generator
    popular_words: list


def get_response_from_google(phrase: str) -> GoogleResult:
    response = requests.get(settings.SEARCH_URL.format(settings.GOOGLE_KEY, phrase))
    json_result = json.loads(response.content)
    text = ' '.join(item['title'] for item in json_result['items'])
    tokens = (token.strip().lower() for token in text.split())
    words = (token for token in tokens if token.isalpha())
    return GoogleResult(
        result_count=int(json_result['searchInformation']['totalResults']),
        urls=(item['link'] for item in json_result['items']),
        popular_words=Counter(words).most_common(10),
    )


def normalize_phrase(phrase: str) -> str:
    return phrase.lower()
