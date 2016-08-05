import threading

from BaseClasses.AMQP.Async.Listener import Worker as amqp_listener
from Server.Users.Workers.AuthorizationEventsUserNotifier.Config import \
    authorization_events_listener as amqp_listener_config
from Server.Users.Workers.AuthorizationEventsUserNotifier.Config import \
    to_users_sender_base as to_users_sender_base_config
from Server.Users.Workers.AuthorizationEventsUserNotifier.EventProcessor import EventProcessor


def main(count_of_workers):
    for i in range(count_of_workers):
        threading.Thread(target=spawn_worker).start()


def spawn_worker():
    event_processor = EventProcessor(to_users_sender_base_config.SEND_TO_PARAMETERS)
    internal_authorization_events_listener = amqp_listener(amqp_listener_config.LISTEN_FROM_PARAMETERS,
                                                           callback=event_processor.process_event)
    internal_authorization_events_listener_thread = threading.Thread(target=internal_authorization_events_listener.run)
    internal_authorization_events_listener_thread.start()


if __name__ == '__main__':
    import logging
    from BaseClasses.AMQP.Async.Listener import LOG_FORMAT

    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
    main(40)
