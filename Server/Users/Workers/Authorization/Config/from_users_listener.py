# Где размещена очередь для прослушивания.
HOST = "192.168.99.100"

# Порт очереди для прослушивания.
PORT = 32778

# Используем ли SSL.
USE_SSL = False

# С какими параметрами используем SSL.
# SSL_OPTIONS = {"ca_certs": "/etc/rabbitmq/testca/cacert.pem",
#                "certfile": "/etc/rabbitmq/client/cert.pem",
#                "keyfile": "/etc/rabbitmq/client/key.pem",
#                "cert_reqs": ssl.CERT_REQUIRED,
#                "server_side": False}
SSL_OPTIONS = ''

# Под каким пользователем заходим.
USER = 'guest'

# Пароль пользователя.
PASSWORD = 'guest'

LISTEN_FROM_PARAMETERS = {
    'url': 'amqp://{0}:{1}@{2}:{3}/%2F'.format(USER, PASSWORD, HOST, PORT),
    'exchange_type': 'topic',
    'exchange': 'login',
    'queue': 'login',
    'routing_key': 'login',
    'prefetch_count': 1
}
