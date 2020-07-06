from collections import Counter, Generator
from dataclasses import dataclass

import requests
from django.conf import settings


@dataclass
class GoogleResult:
    result_count: int
    urls: Generator
    popular_words: list


def get_response_from_google(phrase: str):
    """Get response from google search in form of python native objects"""
    response = requests.get(settings.SEARCH_URL.format(phrase=phrase))
    return response.json()


def _get_words(items):
    """Get the most common words from google results"""
    titles = ' '.join(item.get('title', '') for item in items)
    descriptions = ' '.join(item.get('snippet', '') for item in items)
    text = f"{titles} {descriptions}"
    tokens = (token.strip('.,-_:;?!').lower() for token in text.split())
    words = (token for token in tokens if token.isalpha())
    return Counter(words).most_common(10)


def get_data_from_google(phrase: str) -> GoogleResult:
    json_result = get_response_from_google(phrase)
    return GoogleResult(
        result_count=int(json_result['searchInformation']['totalResults']),
        urls=(item.get('link', '') for item in json_result['items']),
        popular_words=_get_words(json_result['items']),
    )


def normalize_phrase(phrase: str) -> str:
    """Normalize the phrase so that similar phrases can be treated as the same phrase"""
    return phrase.lower()
