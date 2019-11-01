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
    # fuzz object inputs
    try:
        usr = objects.User(username=username,
                           raw_password=raw_password,
                           user_id=user_id)

        # Check that get_safe_id always returns a string
        assert (isinstance(usr.get_safe_id(), str))
        # Check that the user_id remains consistent
        assert (usr.get_safe_id() == str(user_id))

        # Validate the password
        assert (usr.validate_password_hash(raw_password))

    # Only throw UserInitializationFailure for
    # exceptions when something goes wrong in
    # during user initialization.
    except exceptions.UserInitializationFailure:
        pass
