import logging

from BaseClasses.AMQP.Async.Sender import Worker as SenderWorker

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)


class Worker(SenderWorker):
    """This is an example publisher that will handle unexpected interactions
    with RabbitMQ such as channel and connection closures.
    If RabbitMQ closes the connection, it will reopen it. You should
    look at the output, as there are limited reasons why the connection may
    be closed, which usually are tied to permission related issues or
    socket timeouts.
    It uses delivery confirmations and illustrates one way to keep track of
    messages that have been sent and if they've been confirmed by RabbitMQ.
    """

    def __init__(self, send_to_parameters, publish_interval, message):
        """Setup the example publisher object, passing in the URL we will use
        to connect to RabbitMQ.
        :param str amqp_url: The URL for connecting to RabbitMQ
        """
        super().__init__(send_to_parameters)

        self._publish_interval = publish_interval
        self._message = message

    def start_publishing(self):
        """This method will enable delivery confirmations and schedule the
        first message to be sent to RabbitMQ
        """
        super().start_publishing()
        self.schedule_next_message()

    def schedule_next_message(self):
        """If we are not closing our connection to RabbitMQ, schedule another
        message to be delivered in PUBLISH_INTERVAL seconds.
        """
        LOGGER.info('Scheduling next message for %0.1f seconds',
                    self._publish_interval)
        self._connection.add_timeout(self._publish_interval,
                                     self.send_my_message)

    def send_my_message(self):
        self.publish_message(self._message)
        self.schedule_next_message()