import logging

import pymongo

from BaseClasses.AMQP.Async.Listener import Worker as amqp_listener
from Databases.Users.Config import db as db_config
from Databases.Users.Workers.UserActivityReporter.Config import amqp as amqp_config
from Databases.Users.Workers.UserActivityReporter.UserActivityReporter import UserActivityReporter

USER_ACTIVITY_REPORTER = UserActivityReporter(
    pymongo.MongoClient(host=db_config.HOST, port=db_config.PORT).project_world
)

AMQP_LISTENER = amqp_listener('amqp://{0}:{1}@{2}:{3}/%2F'.format(amqp_config.USER,
                                                                  amqp_config.PASSWORD,
                                                                  amqp_config.HOST,
                                                                  amqp_config.PORT),
                              exchange=amqp_config.EXCHANGE,
                              exchange_type=amqp_config.EXCHANGE_TYPE,
                              queue=amqp_config.QUEUE,
                              routing_key=amqp_config.ROUTING_KEY,
                              prefetch_count=amqp_config.PREFETCH_COUNT,
                              callback=USER_ACTIVITY_REPORTER.do_command)

if __name__ == '__main__':
    from BaseClasses.AMQP.Async.Listener import LOG_FORMAT

    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
    AMQP_LISTENER.run()
