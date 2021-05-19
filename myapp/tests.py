import pytest
from django.contrib.auth.models import User


@pytest.mark.django_db
class TestClassScopedFixture:
    @pytest.fixture(scope="class")
    def user_something(self, db_scope_class):
        return User.objects.create_user(
            username="something",
            email="someone@example.com",
            password="thisisnotsafe",
        )

    def test_a(self, user_something):
        assert User.objects.count() == 1

    def test_b(self, user_something):
        assert User.objects.count() == 1
