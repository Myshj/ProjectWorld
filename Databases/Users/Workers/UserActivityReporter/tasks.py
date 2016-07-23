import pymongo
from celery import Celery

from Databases.Users.Config import db as db_config

app = Celery()
app.config_from_object('Databases.Users.Workers.UserActivityReporter.celeryconfig')

mongo_client = pymongo.MongoClient(host=db_config.HOST, port=db_config.PORT)

db = mongo_client.project_world


@app.task
def report_user_activity(login, password):
    """
    Notifies that user has connection to the server.
    :param str login:
    :param str password:
    :return bool: True if notified successfully. False otherwise.
    """
    return db.users.update_one({'login': login, 'password': password},
                               {'$currentDate': {'last_activity': True}}).modified_count == 1
