import configparser
import redis
import json
import glob
from .objects import User
from .constants import SaveState

config = configparser.ConfigParser()
config.read('config/defaults.ini')

POOL = redis.ConnectionPool(host=config['redis']['hostname'],
                            port=config['redis']['port'])
CON = None

SCRIPTS = dict()


def _get_connection():
    global POOL
    global CON
    global SCRIPTS

    if not CON:
        CON = redis.Redis(connection_pool=POOL)

        files = glob.glob('scripts/*.lua')

        for file in files:
            SCRIPTS[file.replace('.lua', '').replace('scripts\\', '')] \
                = CON.register_script(open(file).read())

    else:
        return CON


def save(obj):
    if isinstance(obj, User):
        _save_user_handler(obj)


def _save_user_handler(user):
    global SCRIPTS
    r = _get_connection()

    if not r.hget('username_to_id', user.username):

        SCRIPTS['new_user'](keys=[user.username,
                                  user.get_safe_id(),
                                  user.password_hash])

        if user.public_values:
            r.hset('id_to_user_properties', user.get_safe_id(),
                   json.loads(user.public_values))

        user._state = SaveState.clean


_get_connection()
