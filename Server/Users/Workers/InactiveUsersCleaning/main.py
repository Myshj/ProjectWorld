import pymongo

from BaseClasses.AMQP.Async.Listener import Worker as amqp_listener
from BaseClasses.AMQP.Async.Sender import Worker as amqp_sender
from Server.Users.Config import db as db_config
from Server.Users.Workers.InactiveUsersCleaning.CommandProcessor import CommandProcessor
from Server.Users.Workers.InactiveUsersCleaning.Config import amqp as amqp_listener_config
from Server.Users.Workers.InactiveUsersCleaning.Config import general as general_config
from Server.Users.Workers.InactiveUsersCleaning.Config import logout_sender as amqp_sender_config

AMQP_SENDER = amqp_sender(send_to_parameters=amqp_sender_config.SEND_TO_PARAMETERS)

AFK_CLEANER = CommandProcessor(
    pymongo.MongoClient(host=db_config.HOST, port=db_config.PORT).project_world,
    AMQP_SENDER,
    general_config
)

AMQP_LISTENER = amqp_listener(listen_from_parameters=amqp_listener_config.LISTEN_FROM_PARAMETERS,
                              callback=AFK_CLEANER.do_command)

if __name__ == '__main__':
    import logging
    from BaseClasses.AMQP.Async.Listener import LOG_FORMAT

    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
    import threading

    sender_thread = threading.Thread(target=AMQP_SENDER.run)
    sender_thread.start()
    AMQP_LISTENER.run()
