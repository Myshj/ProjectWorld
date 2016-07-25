import pymongo

from BaseClasses.AMQP.Async.Listener import Worker as amqp_listener
from BaseClasses.AMQP.Async.Sender import Worker as amqp_sender
from Databases.Users.Config import db as db_config
from Databases.Users.Workers.AfkCleaner.AfkCleaner import AfkCleaner
from Databases.Users.Workers.AfkCleaner.Config import amqp as amqp_listener_config
from Databases.Users.Workers.AfkCleaner.Config import general as general_config
from Databases.Users.Workers.AfkCleaner.Config import logout_sender as amqp_sender_config

AMQP_SENDER = amqp_sender('amqp://{0}:{1}@{2}:{3}/%2F'.format(amqp_sender_config.USER,
                                                              amqp_sender_config.PASSWORD,
                                                              amqp_sender_config.HOST,
                                                              amqp_sender_config.PORT),
                          exchange=amqp_sender_config.EXCHANGE,
                          exchange_type=amqp_sender_config.EXCHANGE_TYPE,
                          queue=amqp_sender_config.QUEUE,
                          routing_key=amqp_sender_config.ROUTING_KEY)

AFK_CLEANER = AfkCleaner(
    pymongo.MongoClient(host=db_config.HOST, port=db_config.PORT).project_world,
    AMQP_SENDER,
    general_config
)

AMQP_LISTENER = amqp_listener('amqp://{0}:{1}@{2}:{3}/%2F'.format(amqp_listener_config.USER,
                                                                  amqp_listener_config.PASSWORD,
                                                                  amqp_listener_config.HOST,
                                                                  amqp_listener_config.PORT),
                              exchange=amqp_listener_config.EXCHANGE,
                              exchange_type=amqp_listener_config.EXCHANGE_TYPE,
                              queue=amqp_listener_config.QUEUE,
                              routing_key=amqp_listener_config.ROUTING_KEY,
                              prefetch_count=amqp_listener_config.PREFETCH_COUNT,
                              callback=AFK_CLEANER.do_command)

if __name__ == '__main__':
    import logging
    from BaseClasses.AMQP.Async.Listener import LOG_FORMAT

    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
    import threading

    sender_thread = threading.Thread(target=AMQP_SENDER.run)
    sender_thread.start()
    AMQP_LISTENER.run()
