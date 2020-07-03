import pytest
from django.contrib import auth as dj_auth
from django.urls import reverse
from rest_framework import status

from . import factories

pytestmark = pytest.mark.django_db


class Test:
    def test_dummy(self):
        pass

