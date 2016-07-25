# Где размещена очередь для прослушивания.
HOST = "192.168.99.100"

# Порт очереди для прослушивания.
PORT = 32778

# Сколько сообщений из очереди резервируем для себя.
PREFETCH_COUNT = 1

# Используем ли SSL.
USE_SSL = False

# С какими параметрами используем SSL.
# SSL_OPTIONS = {"ca_certs": "/etc/rabbitmq/testca/cacert.pem",
#                "certfile": "/etc/rabbitmq/client/cert.pem",
#                "keyfile": "/etc/rabbitmq/client/key.pem",
#                "cert_reqs": ssl.CERT_REQUIRED,
#                "server_side": False}
SSL_OPTIONS = ''

# Имя очереди для прослушивания.
QUEUE = "user_activity"

# Имя точки обмена.
EXCHANGE = 'user_activity'

# Какие сообщения будем получать.
ROUTING_KEY = 'user_activity'

# Тип точки обмена.
EXCHANGE_TYPE = 'topic'

# Под каким пользователем заходим.
USER = 'guest'

# Пароль пользователя.
PASSWORD = 'guest'
