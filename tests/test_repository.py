import pytest
from flaskcap import repository
from flaskcap import objects


def test_user_save():
    x = objects.User(username='User1',
                     raw_password='HunterDos')

    repository.save(x)
