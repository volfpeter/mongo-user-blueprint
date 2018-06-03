"""
Demo `Flask` application showing how to use the `user-blueprint` project to set up a
MongoDB-based user handling web application.

Note that you will need a MongoDB instance to connect to. If you don't your own
database, sign up to a service that provides free demo MongoDB databases, such as
mLab (mlab.com).
"""


# Imports
# ----------------------------------------


from flask import Flask, url_for

from flask_login import LoginManager,\
                        current_user,\
                        login_required

from user_blueprint.blueprint import user_blueprint, user_handler
from user_blueprint.user import console_password_reset_email_sender,\
                                console_verification_email_sender

from mongo_user_blueprint.mongoutil import ServerDescriptor,\
                                           DatabaseDescriptor,\
                                           CollectionDescriptor
from mongo_user_blueprint.user import User,\
                                      configure_login_manager,\
                                      configure_user_handler


# Metadata
# ------------------------------------------------------------


__author__ = 'Peter Volf'


# Database configuration
# ----------------------------------------


mongodb_url: str = "databaseurl.db"
mongodb_port: int = 12345
database_name: str = "userdemo"
database_username: str = "demo"
database_password: str = "password"

server: ServerDescriptor = ServerDescriptor(mongodb_url, mongodb_port)
database: DatabaseDescriptor = DatabaseDescriptor(server, database_name, database_username, database_password)
user_collection: CollectionDescriptor[User] = CollectionDescriptor[User](database, User, "users")


# Application configuration
# ----------------------------------------


app = Flask(__name__)
app.secret_key = "mongo-user-blueprint application secret key"
app.register_blueprint(user_blueprint, url_prefix="/auth")


# Login manager configuration
# ----------------------------------------


login_manager: LoginManager = LoginManager(app)
login_manager.login_view = "auth.login"
configure_login_manager(login_manager, user_collection)


# User handler configuration
# ----------------------------------------


user_handler.token_signing_key = "user-blueprint user_handler token signing key"
user_handler.password_reset_email_sender(console_password_reset_email_sender)
user_handler.verification_email_sender(console_verification_email_sender)
configure_user_handler(user_handler, user_collection)


# View definitions
# ------------------------------------------------------------


@app.route("/")
@login_required
def index():
    user: User = current_user
    return \
        "<div>" +\
        f"<a href=\"{url_for('auth.logout')}\">Log out</a>" +\
        f"<h1>Welcome {user.username}</h1>" +\
        "</div>"
