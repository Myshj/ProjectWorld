from datetime import datetime

import pymongo
from celery import Celery

import Databases.Users.Workers.AfkCleaner.config as cleaner_config
from Databases.Users.Config import db as db_config

app = Celery()
app.config_from_object('Databases.Users.Workers.AfkCleaner.celeryconfig')

mongo_client = pymongo.MongoClient(host=db_config.HOST, port=db_config.PORT)
db = mongo_client.project_world


@app.task
def clean_afk_users():
    """
    Logs out users that are AFK.
    """
    res = db.users.update({'online': True,
                           'last_activity': {
                               '$lt': (datetime.utcnow() - cleaner_config.MAX_INACTIVITY_PERIOD)}},
                          {'$set': {'online': False}})
