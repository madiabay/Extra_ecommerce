import pytest
from django.core.management import call_command
from rest_framework.test import APIClient

@pytest.fixture()
def api_client():
    return APIClient()

@pytest.fixture()
def load_fixtures():
    return _load_fixtures

def _load_fixtures(*fixtures):
    call_command('loaddata', *fixtures)