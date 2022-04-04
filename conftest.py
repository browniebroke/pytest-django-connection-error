import functools

import pytest
from django.test import TestCase


@pytest.fixture(scope="class")
def db_scope_class(request, django_db_setup, django_db_blocker):
    yield from _db_fixture_helper(request, django_db_blocker)


def _db_fixture_helper(request, django_db_blocker):
    with django_db_blocker.unblock():
        request.addfinalizer(django_db_blocker.restore)

        atomics = TestCase._enter_atomics()
        request.addfinalizer(functools.partial(TestCase._rollback_atomics, atomics))
        yield


@pytest.fixture(autouse=True)
def force_test_db_isolation(request):
    if {"db_scope_class"}.intersection(request.fixturenames):
        request.getfixturevalue("db")
