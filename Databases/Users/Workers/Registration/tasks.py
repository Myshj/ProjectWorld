import datetime

import pymongo
from celery import Celery

from Databases.Users.Config import db as db_config

app = Celery()
app.config_from_object('Databases.Users.Workers.Registration.celeryconfig')

mongo_client = pymongo.MongoClient(host=db_config.HOST, port=db_config.PORT)

db = mongo_client.project_world

db.users.create_index([('login', pymongo.ASCENDING)], unique=True)


@app.task
def register_user(login, password, emails):
    """
    Tries to register new user.
    :param str login: Login for user.
    :param str password: Password for user.
    :param [str] emails: Emails for user.
    :return bool: True if user registered. False otherwise.
    """
    try:
        db.users.insert_one({'login': login,
                             'password': password,
                             'emails': emails,
                             'online': False,
                             'last_activity': datetime.datetime.utcnow()})
        return True
    except:
        return False


@app.task
def remove_user(login, password):
    """
    Tries to remove user.
    :param str login: User's login.
    :param str password: User's password.
    :return bool: True if user removed successfully. False otherwise.
    """
    return db.users.delete_many({'login': login, 'password': password}).deleted_count == 1
