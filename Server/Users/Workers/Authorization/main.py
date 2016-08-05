import threading

import pymongo

from BaseClasses.AMQP.Async.Listener import Worker as amqp_listener
from BaseClasses.AMQP.Async.Sender import Worker as amqp_sender
from Server.Users.Config import db as db_config
from Server.Users.Workers.Authorization.CommandProcessor import CommandProcessor
from Server.Users.Workers.Authorization.Config import authorization_events_sender as authorization_events_sender_config
from Server.Users.Workers.Authorization.Config import from_users_listener as amqp_listener_config
from Server.Users.Workers.Authorization.Config import user_activity_sender as user_activity_sender_config


def main(count_of_workers):
    for i in range(count_of_workers):
        threading.Thread(target=spawn_worker).start()


def spawn_worker():
    user_activity_reports_sender = spawn_user_activity_reports_sender()
    authorization_reports_sender = spawn_authorization_reports_sender()
    mongo_client = pymongo.MongoClient(host=db_config.HOST, port=db_config.PORT).project_world
    command_processor = CommandProcessor(mongo_client,
                                         user_activity_reports_sender,
                                         authorization_reports_sender)
    authorization_events_listener = amqp_listener(amqp_listener_config.LISTEN_FROM_PARAMETERS,
                                                  callback=command_processor.do_command)
    authorization_events_listener_thread = threading.Thread(target=authorization_events_listener.run)
    authorization_events_listener_thread.start()


def spawn_authorization_reports_sender():
    authorization_reports_sender = amqp_sender(
        send_to_parameters=authorization_events_sender_config.SEND_TO_PARAMETERS)
    authorization_reports_sender_thread = threading.Thread(target=authorization_reports_sender.run)
    authorization_reports_sender_thread.start()
    return authorization_reports_sender


def spawn_user_activity_reports_sender():
    user_activity_reports_sender = amqp_sender(send_to_parameters=user_activity_sender_config.SEND_TO_PARAMETERS)
    user_activity_reports_sender_thread = threading.Thread(target=user_activity_reports_sender.run)
    user_activity_reports_sender_thread.start()
    return user_activity_reports_sender


if __name__ == '__main__':
    import logging
    from BaseClasses.AMQP.Async.Listener import LOG_FORMAT

    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
    main(40)
