import pymongo

from Databases.Users.Config import db as db_config
from Databases.Users.Workers.UserActivityReporter.tasks import report_user_activity

mongo_client = pymongo.MongoClient(host=db_config.HOST, port=db_config.PORT)

db = mongo_client.project_world


def login_user(login, password):
    """
    Tries to log user in.
    :param str login: User's login.
    :param str password: User's password.
    :return None.
    """
    report_user_activity.delay(login, password)
    db.users.update_one({'login': login, 'password': password},
                        {'$set': {'online': True}})


def logout_user(login, password):
    """
    Tries to log user out.
    :param str login: User's login.
    :param str password: User's password.
    :return None.
    """
    report_user_activity.delay(login, password)
    db.users.update_one({'login': login, 'password': password},
                        {'$set': {'online': False}})


def do_command(command):
    """
    Performs command described in dictionary.
    :param dict command: Command to perform.
    :return:
    """
    try:
        if command['action'] == 'login':
            login_user(command['login'], command['password'])
        elif command['action'] == 'logout':
            logout_user(command['login'], command['password'])
    except:
        pass
