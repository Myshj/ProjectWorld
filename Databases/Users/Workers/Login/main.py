import pymongo

from BaseClasses.AMQP.Async.Listener import Worker as amqp_listener
from BaseClasses.AMQP.Async.Sender import Worker as amqp_sender
from Databases.Users.Config import db as db_config
from Databases.Users.Workers.Login.Config import login_listener as amqp_listener_config
from Databases.Users.Workers.Login.Config import user_activity_sender as amqp_sender_config
from Databases.Users.Workers.Login.Loginer import Loginer

AMQP_SENDER = amqp_sender(send_to_parameters=amqp_sender_config.SEND_TO_PARAMETERS)

LOGINER = Loginer(
    pymongo.MongoClient(host=db_config.HOST, port=db_config.PORT).project_world,
    AMQP_SENDER
)

AMQP_LISTENER = amqp_listener(amqp_listener_config.LISTEN_FROM_PARAMETERS,
                              callback=LOGINER.do_command)

if __name__ == '__main__':
    import logging
    from BaseClasses.AMQP.Async.Listener import LOG_FORMAT

    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
    import threading

    sender_thread = threading.Thread(target=AMQP_SENDER.run)
    sender_thread.start()
    AMQP_LISTENER.run()
