import pytest
from hypothesis import given, settings
from hypothesis.strategies import text
from hypothesis.strategies import uuids
from flaskcap import objects
from flaskcap import exceptions

# Only want to create this once some tests,
# but want test_user_create to fail instead
# of this throwing an exception if it's
# screwed up.
try:
    test_user = objects.User(username='test_user',
                             raw_password='test_password',
                             public_values={'age': 18},
                             private_values={'group': 'admins'})
except Exception as ex:
    pass


def test_user_create():
    assert objects.User(username='test_user',
                        raw_password='test_password',
                        public_values={'age': 18},
                        private_values={'group': 'admins'})


def test_user_create_benchmark(benchmark):
    def _get_user():
        objects.User(username='test_user',
                     raw_password='test_password',
                     public_values={'age': 18},
                     private_values={'group': 'admins'})

    benchmark(_get_user)


def test_user_password_validation_benchmark(benchmark):
    global test_user
    benchmark(test_user.validate_password_hash, 'test_password')


def test_user_get_safe_id_benchmark(benchmark):
    global test_user
    # clear id to test generation speed
    test_user._clear_id()
    benchmark(test_user.get_safe_id)


@given(username=text(),
       raw_password=text(),
       user_id=uuids())
@settings(deadline=None)
@pytest.mark.fuzz
def test_user_create_fuzz(username,
                          raw_password,
                          user_id):
    # Fuzz object inputs for undefined behavior
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
