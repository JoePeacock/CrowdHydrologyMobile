import arrow
from sqlalchemy_utils import EmailType, ArrowType, PasswordType

from app import db


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(EmailType, unique=True, nullable=False)
    password = db.Column(PasswordType(schemes=['pbkdf2_sha512', 'md5_crypt'],
                                      deprecated=['md5_crypt']),
                         nullable=False)

    created_at = db.Column(ArrowType, default=arrow.utcnow)
    admin = db.Column(db.Boolean)

    def __init__(self, **kwargs):
        self.__dict__.update(**kwargs)

    def get_id(self):
        """
        Requirement for Flask-Login
        :return: unicode object that uniquely identifies this user
        """
        return unicode(self.id)

    def is_authenticated(self):
        """
        Requirements for Flask-Login
        :return: whether this user is authenticated or not.
        """
        return True

    def is_active(self):
        """
        Check the current interger state. Refer to config/user_state for
        settings. 0 is inactive, 1 is active and valid email. Greater than 1 is
        some other defined state.
        :return:  Boolean of the user_state
        """
        return True

    def is_anonymous(self):
        """
        If this session is anon or not. Clearly not. Will always be false.
        :return: Actual user will always return false.
        """
        return False
