import pytest
from hypothesis import given, settings
from hypothesis.strategies import text
from hypothesis.strategies import uuids
from flaskcap import objects
from flaskcap import exceptions


def _create_test_user():
    return objects.User(username='test_user',
                        raw_password='test_password',
                        public_values={'age': 18},
                        private_values={'group': 'admins'})


def test_user_create(benchmark):
    benchmark(_create_test_user)


def test_user_password_validation(benchmark):
    usr = _create_test_user()
    benchmark(usr.validate_password_hash, 'test_password')


def test_user_get_safe_id(benchmark):
    usr = _create_test_user()
    benchmark(usr.get_safe_id)


@given(username=text(),
       raw_password=text(),
       user_id=uuids())
@settings(deadline=None)
@pytest.mark.fuzz
def test_user_create_fuzz(username,
                          raw_password,
                          user_id):
    try:
        usr = objects.User(username=username,
                           raw_password=raw_password,
                           user_id=user_id)

        assert (usr.get_safe_id() == user_id)

        assert (usr.validate_password_hash(raw_password))

    except exceptions.UserInitializationFailure:
        pass

    try:
        usr = objects.User(username=username,
                           raw_password=raw_password,
                           user_id=user_id)

        assert (usr.get_safe_id() == user_id)
        assert (usr.validate_password_hash(raw_password))

    except exceptions.UserInitializationFailure:
        pass
