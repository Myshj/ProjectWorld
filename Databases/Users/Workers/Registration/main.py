import logging

import pymongo

from BaseClasses.AMQP.Async.Listener import Worker as amqp_listener
from Databases.Users.Config import db as db_config
from Databases.Users.Workers.Registration.Config import amqp as amqp_config
from Databases.Users.Workers.Registration.Registrationer import Registrationer

REGISTRATIONER = Registrationer(
    pymongo.MongoClient(host=db_config.HOST, port=db_config.PORT).project_world
)

AMQP_LISTENER = amqp_listener(amqp_config.LISTEN_FROM_PARAMETERS,
                              callback=REGISTRATIONER.do_command)

if __name__ == '__main__':
    from BaseClasses.AMQP.Async.Listener import LOG_FORMAT

    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
    AMQP_LISTENER.run()
