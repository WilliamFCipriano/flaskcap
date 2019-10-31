import configparser
import redis
from .objects import User

config = configparser.ConfigParser()
config.read('config/defaults.ini')


def _get_connection():
    return redis.Redis(
        host=config['redis']['hostname'],
        port=config['redis']['port']
    )


def save(obj):
    if isinstance(obj, User):
        _save_user_handler(obj)


def _save_user_handler(user):
    r = _get_connection()

    if not r.hget('username_to_id', user.username):
        r.hset('username_to_id', user.username, str(user.get_safe_id()))
        r.hset('id_to_username', user.get_safe_id(), user.username)
