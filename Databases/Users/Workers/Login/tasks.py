import pymongo
from celery import Celery

from Databases.Users.Config import db as db_config
from Databases.Users.Workers.UserActivityReporter.tasks import report_user_activity

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
    report_user_activity.delay(login, password)
    return db.users.update_one({'login': login, 'password': password},
                               {'$set': {'online': True}}).modified_count == 1


@app.task
def logout_user(login, password):
    """
    Tries to log user out.
    :param str login: User's login.
    :param str password: User's password.
    :return bool: True if user logged out. False otherwise.
    """
    report_user_activity.delay(login, password)
    return db.users.update_one({'login': login, 'password': password},
                               {'$set': {'online': False}}).modified_count == 1
