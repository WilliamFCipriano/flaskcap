import configparser
import redis
import json
import glob
from datetime import datetime
from .objects import User
from .constants import SaveState

config = configparser.ConfigParser()
config.read('config/flaskcap.ini')

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
        files = glob.glob('%s/*.lua' %
                          config['redis']['scripts_location'])
        for file in files:
            SCRIPTS[file.replace('.lua', '').replace('lua\\', '')] \
                = CON.register_script(open(file).read())
    else:
        return CON


def _run_script(script_name, keys=None):
    if keys is not None:
        return SCRIPTS[script_name](keys=keys)
    else:
        return SCRIPTS[script_name]()


def save(obj):
    if isinstance(obj, User):
        _save_user_handler(obj)


def _save_user_handler(user):
    global SCRIPTS

    _run_script('save_user', keys=[user.username,
                                   user.get_safe_id(),
                                   user.password_hash,
                                   datetime.utcnow().strftime('%x %X')])

    user._state = SaveState.clean


_get_connection()
