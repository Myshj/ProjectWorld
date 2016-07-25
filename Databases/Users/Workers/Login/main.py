import pymongo

from BaseClasses.AMQP.Async.Listener import Worker as amqp_listener
from BaseClasses.AMQP.Async.Sender import Worker as amqp_sender
from Databases.Users.Config import db as db_config
from Databases.Users.Workers.Login.Config import login_listener as amqp_listener_config
from Databases.Users.Workers.Login.Config import user_activity_sender as amqp_sender_config
from Databases.Users.Workers.Login.Loginer import Loginer

AMQP_SENDER = amqp_sender('amqp://{0}:{1}@{2}:{3}/%2F'.format(amqp_sender_config.USER,
                                                              amqp_sender_config.PASSWORD,
                                                              amqp_sender_config.HOST,
                                                              amqp_sender_config.PORT),
                          exchange=amqp_sender_config.EXCHANGE,
                          exchange_type=amqp_sender_config.EXCHANGE_TYPE,
                          queue=amqp_sender_config.QUEUE,
                          routing_key=amqp_sender_config.ROUTING_KEY)

LOGINER = Loginer(
    pymongo.MongoClient(host=db_config.HOST, port=db_config.PORT).project_world,
    AMQP_SENDER
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
                              callback=LOGINER.do_command)

if __name__ == '__main__':
    import logging
    from BaseClasses.AMQP.Async.Listener import LOG_FORMAT

    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
    import threading

    sender_thread = threading.Thread(target=AMQP_SENDER.run)
    sender_thread.start()
    AMQP_LISTENER.run()
