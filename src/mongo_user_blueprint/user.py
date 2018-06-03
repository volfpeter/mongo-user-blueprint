"""
User database schema definition and related components.
"""


# Imports
# ----------------------------------------


from datetime import date

from flask_login import LoginManager

import pymongo

from pyt.mongoutil import CollectionDescriptor, DatabaseDescriptor, MainDocument

from user_blueprint.user import RegistrationData, UserHandler

# Typing imports
# ----------------------------------------


from typing import Dict, List, Optional


# Metadata
# ------------------------------------------------------------


__author__ = 'Peter Volf'


# Classes
# ----------------------------------------


class UserState(object):

    PENDING_VERIFICATION = 1
    """
    The user has registered but has not verified the registration yet.
    """

    ACTIVE = 2
    """
    The user has registered and completed the verification process.
    """


class User(MainDocument):
    """
    Class representing a user in a `Flask-Login`-compatible way.
    """

    __slots__ = ("email", "first_name", "last_name", "password",
                 "registration_date", "state", "username")

    # Static methods
    # ----------------------------------------

    @staticmethod
    def get_index_models() -> List[pymongo.IndexModel]:
        """
        Returns the index models the collection storing this kind of documents should have.
        """
        return [
            pymongo.IndexModel(
                ["email", pymongo.TEXT], unique=True, name="email_index"
            ),
            pymongo.IndexModel(
                ["username", pymongo.TEXT], unique=True, name="username_index"
            )
        ]

    # Initialization
    # ----------------------------------------

    def __init__(self) -> None:
        """
        Initialization.
        """
        super().__init__()

        self.email: str = ""
        """
        The email address of the user.
        """

        self.first_name: str = ""
        """
        The first name of the user.
        """

        self.last_name: str = ""
        """
        The last name of the user.
        """

        self.password: str = ""
        """
        The hashed password of the user.
        """

        self.registration_date: int = date.today().toordinal()
        """
        The registration date as a day ordinal.
        """

        self.username: str = ""
        """
        The username of the user.
        """

        self.state: int = UserState.PENDING_VERIFICATION
        """
        The user's current state. Possible values are listed in the `UserState` class.
        """

    # Dunder methods
    # ----------------------------------------

    def __eq__(self, other: object) -> bool:
        if isinstance(other, User):
            return self._id == other._id
        return NotImplemented

    def __ne__(self, other: object) -> bool:
        if isinstance(other, User):
            return self._id != other._id
        return NotImplemented

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}<"\
            f"email={self.email},username={self.username},"\
            f"first_name={self.first_name},last_name={self.last_name}"\
            f"registration_date={date.fromordinal(self.registration_date)},state={self.state}>"

    # Flask-Login user properties
    # ----------------------------------------

    @property
    def is_active(self) -> bool:
        """
        Whether this is an active user.

        `Flask_login` documentation: This property should return `True` if this is an active user -
        in addition to being authenticated, they also have activated their account, not been
        suspended, or any condition your application has for rejecting an account. Inactive
        accounts may not log in (without being forced of course).
        """
        return self.state == UserState.ACTIVE

    @property
    def is_anonymus(self) -> bool:
        """
        Whether this is an anonymus user and not an authenticated one.

        `Flask_login` documentation: This property should return `True` if this is an anonymous user.
        Actual users should return `False` instead.
        """
        return False

    @property
    def is_authenticated(self) -> bool:
        """
        Whether this is an authenticated user and not an anonymus one.

        `Flask_login` documentation: This property should return `True` if the user is authenticated,
        i.e. they have provided valid credentials. Only authenticated users will fulfill the
        criteria of `login_required`.
        """
        return True

    # Flask-Login user methods
    # ----------------------------------------

    def get_id(self) -> str:
        """
        Returns the ID of the user.

        `Flask_login` documentation: This method must return a unicode that uniquely identifies this
        user, and can be used to load the user from the `user_loader` callback. Note that this must
        be a `unicode` - if the ID is natively an `int` or some other type, you will need to convert
        it to unicode.
        """
        return str(self._id)

    # MongoDocument methods
    # ----------------------------------------

    def to_mongo(self) -> Dict:
        result: Dict = super().to_mongo()

        result["email"] = self.email
        result["first_name"] = self.first_name
        result["last_name"] = self.last_name
        result["password"] = self.password
        result["registration_date"] = self.registration_date
        result["state"] = self.state
        result["username"] = self.username

        return result

    def from_mongo(self, data: Dict) -> None:
        super().from_mongo(data)

        self.email = data["email"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.password = data["password"]
        self.registration_date = data["registration_date"]
        self.state = data["state"]
        self.username = data["username"]


# Methods
# ----------------------------------------


def configure_login_manager(login_manager: LoginManager,
                            user_collection: CollectionDescriptor) -> None:
    """
    Configures the given Flask-Login `LoginManager` to work with the given MongoDB `User` collection.

    Arguments:
        login_manager (LoginManager): The login manager instance to configure.
        user_collection (CollectionDescriptor): The `User` collection the login manager should work with.
    """

    @login_manager.user_loader
    def find_by_id(user_id: str) -> Optional[User]:
        """
        Returns the user that has the given ID in the database.

        Arguments:
            user_id (str): The ID of the user to fetch from the database.

        Returns:
            The user that has the given ID or `None` if no such user exists.
        """
        return user_collection.find_by_id(user_id)


def configure_user_handler(user_handler: UserHandler,
                           user_collection: CollectionDescriptor) -> None:
    """
    Configures the given `UserHandler` to work with the given MongoDB `User` collection.

    Arguments:
        user_handler (UserHandler): The user handler instance to configure.
        user_collection (CollectionDescriptor): The `User` collection the user handler should work with.
    """

    @user_handler.user_by_reset_key_getter
    @user_handler.user_getter
    def get_user_by_identifier(identifier: str) -> Optional[User]:
        """
        Returns the user corresponding to the given identifier (username or email address).

        Arguments:
            identifier (str): The identifier (username or email address) of the user to fetch.

        Returns:
            The user corresponding to the given username or email address if such a user exists.
        """
        prop = "email" if "@" in identifier else "username"
        return user_collection.find_one({prop: identifier})

    @user_handler.reset_key_getter
    def get_user_identifier(user: User) -> str:
        """
        Returns the identifier of the given user.

        Arguments:
            user (User): The user whose identifier is required.

        Returns:
            The identifier of the given user.
        """
        return user.email

    @user_handler.password_getter
    def get_user_password(user: User) -> str:
        """
        Returns the password of the given user.

        Arguments:
            user (User): The user whose password is required.

        Returns:
            The password of the given user.
        """
        return user.password

    @user_handler.user_inserter
    def insert_user(data: RegistrationData) -> bool:
        """
        Inserts the user specified by the given registration form data to the database.

        Arguments:
            data (RegistrationData): The registration form data of the user to create.

        Returns:
            Whether the user has been created successfully.
        """
        user: User = User()
        user.username = data.username
        user.email = data.email
        user.first_name = data.first_name
        user.last_name = data.last_name
        user.password = data.password

        result: pymongo.results.InsertOneResult = user_collection.collection.insert_one(user.to_mongo())
        return result.acknowledged and result.inserted_id is not None

    @user_handler.verification_checker
    def is_user_verified(user: User) -> bool:
        """
        Returns whether the given user's registration is verified.

        Arguments:
            user (User): The user to check.

        Returns:
            Whether the given user's registration is verified.
        """
        return user.is_active

    @user_handler.password_updater
    def update_user_password(user: User, password_hash: str) -> bool:
        """
        Updates the password of the given user to the specified value.

        Arguments:
            user (User): The user whose password is to be updated.
            password_hash (str): The new password hash of the user.

        Returns:
            Whether the user's password has been updated successfully.
        """
        user.password = password_hash
        result: pymongo.results.UpdateResult = user_collection.collection.update_one(
            {"_id": user.id},
            {"$set": {"password": user.password}}
        )
        return result.acknowledged and result.modified_count == 1

    @user_handler.registration_verifier
    def verify_registration(user: User) -> bool:
        """
        Verifies the given user's registration.

        Arguments:
            user (User): The user whose registration is to be verified.

        Returns:
            Whether the user's status has been updated successfully.
        """
        if user.state != UserState.PENDING_VERIFICATION:
            return False

        user.state = UserState.ACTIVE
        result: pymongo.results.UpdateResult = user_collection.collection.update_one(
            {"_id": user.id},
            {"$set": {"state": user.state}}
        )

        return result.acknowledged and result.modified_count == 1


def create_user_collection(database: DatabaseDescriptor,
                        collection_name: str,
                        login_manager: LoginManager,
                        user_handler: UserHandler) -> CollectionDescriptor:
    """
    Creates a collection descriptor for the `User` model and configures the given login manager and
    user handler to work with this collection.

    Arguments:
        database (DatabaseDescriptor): The descriptor of the database that has the collection.
        collection_name (str): The name of the user collection.
        login_manager (LoginManager): The login manager to configure.
        user_handler (UserHandler): The user handler to configure.
    """
    collection: CollectionDescriptor = CollectionDescriptor[User](database, User, collection_name)
    configure_login_manager(login_manager, collection)
    configure_user_handler(user_handler, collection)
    return collection
