import logging

from BaseClasses.AMQP.Async.PeriodicSender import Worker as amqp_periodic_sender
from Databases.Users.Periodics.AfkCleaner.Config import amqp as amqp_config
from Databases.Users.Periodics.AfkCleaner.Config import general as general_config

PERIODIC_AFK_CLEANER = amqp_periodic_sender(amqp_config.SEND_TO_PARAMETERS,
                                            publish_interval=general_config.INTERVAL,
                                            message=general_config.MESSAGE_TO_SEND)

if __name__ == '__main__':
    from BaseClasses.AMQP.Async.Listener import LOG_FORMAT

    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
    PERIODIC_AFK_CLEANER.run()
