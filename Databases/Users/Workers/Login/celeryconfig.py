from kombu import Queue, Exchange

# Broker settings.
BROKER_URL = 'amqp://guest:guest@192.168.99.100:32778//'

# List of modules to import when celery starts.
CELERY_IMPORTS = ('Databases.Users.Workers.Login.tasks',)

# Using the rpc to store task state and results.
CELERY_RESULT_BACKEND = 'rpc://'

# Serializing and receiving only JSON.
CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'

CELERY_DEFAULT_QUEUE = 'login'
CELERY_QUEUES = (
    Queue('login', Exchange('login'), routing_key='login'),
)
