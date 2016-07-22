import pymongo
from celery import Celery

from Databases.Users.Config import db as db_config

app = Celery()
app.config_from_object('Databases.Users.Workers.Login.celeryconfig')

mongo_client = pymongo.MongoClient(host=db_config.HOST, port=db_config.PORT)

db = mongo_client.project_world


@app.task
def login_user(login, password):
    """
    Tries to log user in.
    :param str login: User's login.
    :param str password: User's password.
    :return bool: True if user logged in. False otherwise.
    """
    return db.users.update_one({'login': login, 'password': password},
                               {'$set': {'online': True},
                                '$currentDate': {'last_activity': True}}).modified_count == 1


@app.task
def logout_user(login, password):
    """
    Tries to log user out.
    :param str login: User's login.
    :param str password: User's password.
    :return bool: True if user logged out. False otherwise.
    """
    return db.users.update_one({'login': login, 'password': password},
                               {'$set': {'online': False},
                                '$currentDate': {'last_activity': True}}).modified_count == 1


@app.task
def user_is_alive(login, password):
    """
    Notifies that user has connection to the server.
    :param str login:
    :param str password:
    :return bool: True if notified successfully. False otherwise.
    """
    return db.users.update_one({'login': login, 'password': password},
                               {'$currentDate': {'last_activity': True}}).modified_count == 1
