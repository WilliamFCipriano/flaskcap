import configparser
import redis
import json
from .objects import User
from .constants import SaveState

config = configparser.ConfigParser()
config.read('config/defaults.ini')

POOL = redis.ConnectionPool(host=config['redis']['hostname'],
                            port=config['redis']['port'])


def _get_connection():
    global POOL
    return redis.Redis(connection_pool=POOL)


def save(obj):
    if isinstance(obj, User):
        _save_user_handler(obj)


def _save_user_handler(user):
    r = _get_connection()

    if not r.hget('username_to_id', user.username):

        r.hset('username_to_id', user.username, user.get_safe_id())
        r.hset('id_to_username', user.get_safe_id(), user.username)
        r.hset('id_to_password_hash', user.get_safe_id(), user.password_hash)

        if user.public_values:
            r.hset('id_to_user_properties', user.get_safe_id(),
                   json.loads(user.public_values))

        user._state = SaveState.clean
