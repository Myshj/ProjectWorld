import logging
import urllib.parse
from multiprocessing import Process

from Client.UserInterfaceInteraction.LoginListener.Config import amqp as LoginListenerAMQPConfig
from Client.UserInterfaceInteraction.LoginListener.Config import worker as LoginListenerWorkerConfig
from Client.UserInterfaceInteraction.LoginListener.login_listener import Worker as LoginListener

login_listener = None


def start_login_listener(login_listener):
    print('maus')
    login_listener.run()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format=LoginListenerWorkerConfig.LOG_FORMAT)

    login_listener = LoginListener('amqp://{0}:{1}@{2}:{3}/%2F?{4}'.format(LoginListenerAMQPConfig.USER,
                                                                           LoginListenerAMQPConfig.PASSWORD,
                                                                           LoginListenerAMQPConfig.HOST,
                                                                           LoginListenerAMQPConfig.PORT,
                                                                           urllib.parse.urlencode(
                                                                               LoginListenerAMQPConfig.SSL_OPTIONS)),
                                   exchange=LoginListenerAMQPConfig.EXCHANGE,
                                   exchange_type=LoginListenerAMQPConfig.EXCHANGE_TYPE,
                                   queue=LoginListenerAMQPConfig.QUEUE,
                                   routing_key=LoginListenerAMQPConfig.ROUTING_KEY,
                                   prefetch_count=LoginListenerAMQPConfig.PREFETCH_COUNT)

    login_listener_process = Process(target=start_login_listener, args=(login_listener,))
    login_listener_process.start()
    login_listener_process.join()
