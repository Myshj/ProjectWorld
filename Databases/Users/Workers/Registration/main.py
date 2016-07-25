import pymongo

from BaseClasses.AMQP.Async.Listener import Worker as amqp_listener
from Databases.Users.Config import db as db_config
from Databases.Users.Workers.Registration.Config import amqp as amqp_config
from Databases.Users.Workers.Registration.Registrationer import Registrationer

REGISTRATIONER = Registrationer(
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
                              callback=REGISTRATIONER.do_command)

if __name__ == '__main__':
    AMQP_LISTENER.run()
