import secrets
import bcrypt
from datetime import datetime
import uuid
from .exceptions import UserInitializationFailure
from .constants import SaveState


class User:
    """The User object represents a User of the system. It is able to validate passwords.

    Attributes:
        username (str or None): The display name of the user
        id  (UUID, str or None): A unique user id
        creation_time (datetime or None): The time this user was first created
        public_values (dict or None): Any number of key-value pairs, publicly visible
        private_values (dict or None): Any number of key-value pairs, server side only
        password_hash (str or None): bcrypt hash of users password
        raw_password  (str or None): The users raw password for comparison purposes

    Methods:
        get_safe_id: safe id get, returns a uuid4 if no id is set
        validate_password_hash: Validates raw_password against the users password_hash
    """

    def __init__(
            self,
            username: object = None,
            raw_password: object = None,
            password_hash: object = None,
            user_id: object = None,
            creation_time: object = None,
            public_values: dict = None,
            private_values: object = None,
    ):

        if public_values is None:
            self.public_values = []
        else:
            self.public_value = public_values

        self._initialization_time = False
        self._state = SaveState.dirty

        self.username = username
        self.id = user_id
        self.creation_time = creation_time
        self.private_values = private_values
        self.password_hash = password_hash
        self.raw_password = raw_password
        self.__validate__()

    def get_safe_id(self) -> str:
        if not self.id:
            self.id = uuid.uuid4()
        return str(self.id)

    def validate_password_hash(self, password):
        if self.password_hash:
            return bcrypt.checkpw(password.encode("utf8"), self.password_hash)
        return False

    def generate_password_hash(self, raw_password):
        self.raw_password = raw_password
        self.password_hash = bcrypt.hashpw(
            raw_password.encode("utf8"), bcrypt.gensalt()
        )

    def __validate__(self,
                     username_req=True,
                     id_req=True,
                     password_req=True):

        self._initialization_time = datetime.now()

        try:
            if id_req:
                id = self.get_safe_id()

            if username_req:
                assert isinstance(self.username, str)

            if password_req:
                if self.password_hash and self.raw_password:
                    assert self.validate_password_hash(self.raw_password)

                elif self.raw_password:
                    self.generate_password_hash(self.raw_password)

                else:
                    raise UserInitializationFailure(
                        "Password required but no password set"
                    )

        except Exception as ex:
            raise UserInitializationFailure(ex)

    # for testability purposes
    def _clear_id(self):
        self.id = None


class Session:
    """The session object represents the user session. It can validate session_tokens.

    Attributes:
        user (User or None): The user the session belongs to
        session_id (str or None): A urlsafe string
        session_token (str or None): A urlsafe string

    Methods:
        validate_token: validate a session token securely
    """

    def __init__(
            self,
            user: object = None,
            session_id: object = None,
            session_token: object = None,
    ):

        self.user = user
        self.session_id = session_id
        self.session_token = session_token

    def validate_token(self, token):
        if secrets.compare_digest(token, self.session_token):
            return True
        return False

    def __eq__(self, other):
        if self.session_id == other.session_id:
            return True
        return False
