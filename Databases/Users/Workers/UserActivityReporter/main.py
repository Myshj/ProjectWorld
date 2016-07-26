import logging

import pymongo

from BaseClasses.AMQP.Async.Listener import Worker as amqp_listener
from Databases.Users.Config import db as db_config
from Databases.Users.Workers.UserActivityReporter.Config import amqp as amqp_config
from Databases.Users.Workers.UserActivityReporter.UserActivityReporter import UserActivityReporter

USER_ACTIVITY_REPORTER = UserActivityReporter(
    pymongo.MongoClient(host=db_config.HOST, port=db_config.PORT).project_world
)

AMQP_LISTENER = amqp_listener(listen_from_parameters=amqp_config.LISTEN_FROM_PARAMETERS,
                              callback=USER_ACTIVITY_REPORTER.do_command)

if __name__ == '__main__':
    from BaseClasses.AMQP.Async.Listener import LOG_FORMAT

    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
    AMQP_LISTENER.run()
