from app import db
from flask_bcrypt import Bcrypt
from flask import current_app
import jwt
from datetime import datetime, timedelta


class User(db.Model):
    """This class defines the users table """

    __tablename__ = 'users'

    # Define the columns of the users table, starting with the primary key
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    paragraph = db.Column(db.String(225))
    label = db.Column(db.String(225))
    textbox = db.Column(db.String(225))
    checkbox = db.Column(db.String(225))
    radiobutton = db.Column(db.String(225))
    dropdown = db.Column(db.String(225))
    rating = db.Column(db.Integer)
    switch = db.Column(db.Integer)
    date = db.Column(db.Date)
    name = db.Column(db.String(255))
    restest1 = db.relationship(
        'Resttesting', order_by='Resttesting.id', cascade="all, delete-orphan")

    def __init__(self, email, password):
        """Initialize the user with an email and a password."""
        self.email = email
        self.password = Bcrypt().generate_password_hash(password).decode()

    def password_is_valid(self, password):
        """
        Checks the password against it's hash to validates the user's password
        """
        return Bcrypt().check_password_hash(self.password, password)

    def save(self):
        """Save a user to the database.
        This includes creating a new user and editing one.
        """
        db.session.add(self)
        db.session.commit()

    def generate_token(self, user_id):
        """Generates the access token to be used as the Authorization header"""

        try:
            # set up a payload with an expiration time
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=5),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            # create the byte string token using the payload and the SECRET key
            jwt_string = jwt.encode(
                payload,
                current_app.config.get('SECRET'),
                algorithm='HS256'
            )
            return jwt_string

        except Exception as e:
            # return an error in string format if an exception occurs
            return str(e)

    @staticmethod
    def decode_token(token):
        """Decode the access token from the Authorization header."""
        try:
            payload = jwt.decode(token, current_app.config.get('SECRET'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return "Expired token. Please log in to get a new token"
        except jwt.InvalidTokenError:
            return "Invalid token. Please register or login"


class Resttesting(db.Model):
    """This class defines the Resttesting table."""

    __tablename__ = 'resttest1'

    # define the columns of the table, starting with its primary key
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    paragraph = db.Column(db.String(225))
    label = db.Column(db.String(225))
    textbox = db.Column(db.String(225))
    checkbox = db.Column(db.String(225))
    radiobutton = db.Column(db.String(225))
    dropdown = db.Column(db.String(225))
    rating = db.Column(db.Integer)
    switch = db.Column(db.Integer)
    date = db.Column(db.Date)
    name = db.Column(db.String(255))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    created_by = db.Column(db.Integer, db.ForeignKey(User.id))

    def __init__(self, name, created_by):
        """Initialize the Resttesting with a name and its creator."""
        self.name = name
        self.created_by = created_by

    def save(self):
        """Save a Resttesting.
        This applies for both creating a new Resttesting
        and updating an existing onupdate
        """
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all(user_id):
        """This method gets all the restest1 for a given user."""
        return Resttesting.query.filter_by(created_by=user_id)

    def delete(self):
        """Deletes a given Resttesting."""
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        """Return a representation of a Resttesting instance."""
        return "<Resttesting: {}>".format(self.name)