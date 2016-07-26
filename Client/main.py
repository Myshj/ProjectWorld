#!/usr/bin/env python

from BaseClasses.AMQP.Async.Listener import Worker as amqp_listener
from Client.UserInterfaceInteraction.Listener.Config import amqp as amqp_config

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


# Сначала нужно ждать сигнала от пользователя на авторизацию.
def main():
    pass


if __name__ == '__main__':
    main()
