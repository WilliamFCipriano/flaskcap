import configparser
import redis
from datetime import datetime
from .objects import User
from .constants import SaveState
from ._scripts import get_scripts

config = configparser.ConfigParser()
config.read('config/flaskcap.ini')

POOL = redis.ConnectionPool(host=config['redis']['hostname'],
                            port=config['redis']['port'])
CON = False

SCRIPTS = dict()


def _get_connection():
    global POOL
    global CON
    global SCRIPTS

    if not CON:
        CON = redis.Redis(connection_pool=POOL)
        base_scripts = get_scripts()
        for name in base_scripts:
            print(name)
            SCRIPTS[name] \
                = CON.register_script(base_scripts[name])
    else:
        return CON


def _run_script(script_name, keys=None):
    global SCRIPTS
    if keys is not None:
        return SCRIPTS[script_name](keys=keys)
    else:
        return SCRIPTS[script_name]()


def save(obj):
    connection = _get_connection()
    if isinstance(obj, User):
        _save_user_handler(obj)


def get_user(id):
    global SCRIPTS
    user_string = _run_script('get_user', keys=[id])


def _save_user_handler(user):
    global SCRIPTS

    _run_script('save_user', keys=[user.username,
                                   user.get_safe_id(),
                                   user.password_hash,
                                   datetime.utcnow().strftime('%x %X')])

    user._state = SaveState.clean
