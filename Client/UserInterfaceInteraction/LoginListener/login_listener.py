# -*- coding: utf-8 -*-

import json
import logging
import threading
import time

from BaseClasses.AMQP.Async.Listener import Worker as AsyncListener
from Client.UserInterfaceInteraction.LoginListener.Config import amqp as AMQP_Config
from Client.UserInterfaceInteraction.LoginListener.Config import worker as worker_config
from Databases.Users.Workers.Login.tasks import login_user, logout_user
from Databases.Users.Workers.UserActivityReporter.tasks import report_user_activity

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)


class Worker(AsyncListener):
    def __init__(self, amqp_url, exchange, exchange_type, queue, routing_key, prefetch_count):
        super(Worker, self).__init__(amqp_url, exchange, exchange_type, queue, routing_key, prefetch_count)
        self._work_thread = None
        self._login = None
        self._password = None
        # self._lock = threading.Lock()

    def on_message(self, unused_channel, basic_deliver, properties, body):
        """Invoked by pika when a message is delivered from RabbitMQ. The
        channel is passed for your convenience. The basic_deliver object that
        is passed in carries the exchange, routing key, delivery tag and
        a redelivered flag for the message. The properties passed in is an
        instance of BasicProperties with the message properties and the body
        is the message that was sent.
        :param pika.channel.Channel unused_channel: The channel object
        :param pika.Spec.Basic.Deliver: basic_deliver method
        :param pika.Spec.BasicProperties: properties
        :param bytes body: The message body
        """
        LOGGER.info('Received message # %s from %s: %s',
                    basic_deliver.delivery_tag, properties.app_id, body.decode('utf-8'))
        super(Worker, self).on_message(unused_channel, basic_deliver, properties, body)
        try:
            body = json.loads(body.decode('utf-8'))
            action = body['action']
            if action == 'login':
                self.on_login_me(body['login'], body['password'])
            elif action == 'logout':
                self.on_logout_me(body['login'], body['password'])
        except:
            LOGGER.info('Received malformed message.')

    def on_logout_me(self, login, password):
        """
        Tries to log user with provided credentials out.
        After successful logout stops reporting user activity to server.
        :param login:
        :param password:
        :return:
        """
        self.set_credentials(login, password)
        logout_user.delay(login, password)
        self._work_thread.running = False
        self._work_thread = None

    def on_login_me(self, login, password):
        """
        Tries to log user with provided credentials in.
        After successful login periodically reports user activity to server.
        :param str login:
        :param str password:
        :return: None
        """
        if login_user.delay(login, password).get(timeout=worker_config.MAX_TIMEOUT):
            self.set_credentials(login, password)
            if self._work_thread is None:
                self._work_thread = threading.Thread(target=self.keep_me_logged_in, args=(), daemon=True)
                self._work_thread.start()

    def set_credentials(self, login, password):
        # with self._lock:
        self._login = login
        self._password = password

    def keep_me_logged_in(self):
        t = threading.current_thread()
        while getattr(t, 'running', True):
            print("The time is %s" % time.ctime())
            # with self._lock:
            report_user_activity.delay(self._login, self._password)
            time.sleep(worker_config.INTERVAL)
        print('stopped')


def main():
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

    example = Worker('amqp://{0}:{1}@{2}:{3}/%2F'.format(AMQP_Config.USER,
                                                         AMQP_Config.PASSWORD,
                                                         AMQP_Config.HOST,
                                                         AMQP_Config.PORT),
                     exchange=AMQP_Config.EXCHANGE,
                     exchange_type=AMQP_Config.EXCHANGE_TYPE,
                     queue=AMQP_Config.QUEUE,
                     routing_key=AMQP_Config.ROUTING_KEY,
                     prefetch_count=AMQP_Config.PREFETCH_COUNT)
    try:
        example.run()
    except KeyboardInterrupt:
        example.stop()


if __name__ == '__main__':
    main()
