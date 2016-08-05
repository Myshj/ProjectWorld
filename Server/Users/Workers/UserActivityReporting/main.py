import threading

import pymongo

from BaseClasses.AMQP.Async.Listener import Worker as amqp_listener
from Server.Users.Config import db as db_config
from Server.Users.Workers.UserActivityReporting.CommandProcessor import CommandProcessor
from Server.Users.Workers.UserActivityReporting.Config import amqp as amqp_listener_config


def main(count_of_workers):
    for i in range(count_of_workers):
        threading.Thread(target=spawn_worker).start()


def spawn_worker():
    mongo_client = pymongo.MongoClient(host=db_config.HOST, port=db_config.PORT).project_world
    command_processor = CommandProcessor(mongo_client)
    activity_events_listener = amqp_listener(amqp_listener_config.LISTEN_FROM_PARAMETERS,
                                             callback=command_processor.do_command)
    activity_events_listener_thread = threading.Thread(target=activity_events_listener.run)
    activity_events_listener_thread.start()


if __name__ == '__main__':
    import logging
    from BaseClasses.AMQP.Async.Listener import LOG_FORMAT

    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
    main(40)
