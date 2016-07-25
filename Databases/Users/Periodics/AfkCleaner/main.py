import logging

from BaseClasses.AMQP.Async.PeriodicSender import Worker as amqp_periodic_sender
from Databases.Users.Periodics.AfkCleaner.Config import amqp as amqp_config
from Databases.Users.Periodics.AfkCleaner.Config import general as general_config

PERIODIC_AFK_CLEANER = amqp_periodic_sender('amqp://{0}:{1}@{2}:{3}/%2F'.format(amqp_config.USER,
                                                                                amqp_config.PASSWORD,
                                                                                amqp_config.HOST,
                                                                                amqp_config.PORT),
                                            exchange=amqp_config.EXCHANGE,
                                            exchange_type=amqp_config.EXCHANGE_TYPE,
                                            queue=amqp_config.QUEUE,
                                            routing_key=amqp_config.ROUTING_KEY,
                                            publish_interval=general_config.INTERVAL,
                                            message=general_config.MESSAGE_TO_SEND)

if __name__ == '__main__':
    from BaseClasses.AMQP.Async.Listener import LOG_FORMAT

    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
    PERIODIC_AFK_CLEANER.run()
