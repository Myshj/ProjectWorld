# Где размещена очередь для прослушивания.
HOST = "192.168.99.100"

# Порт очереди для прослушивания.
PORT = 32778

# Имя очереди для прослушивания.
QUEUE = "from_user_interface"

# Сколько сообщений из очереди резервируем для себя.
PREFETCH_COUNT = 1

# Используем ли SSL.
USE_SSL = False

PUBLISH_INTERVAL = 0.1

# С какими параметрами используем SSL.
# SSL_OPTIONS = {"ca_certs": "/etc/rabbitmq/testca/cacert.pem",
#                "certfile": "/etc/rabbitmq/client/cert.pem",
#                "keyfile": "/etc/rabbitmq/client/key.pem",
#                "cert_reqs": ssl.CERT_REQUIRED,
#                "server_side": False}

# Имя точки обмена.
EXCHANGE = 'from_user_interface'

# Тип точки обмена.
EXCHANGE_TYPE = 'topic'

# Какие сообщения будем получать.
ROUTING_KEY = 'login'

# Под каким пользователем заходим.
USER = 'guest'

# Пароль пользователя.
PASSWORD = 'guest'
