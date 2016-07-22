from kombu import Exchange, Queue

# Broker settings.
BROKER_URL = 'amqp://guest:guest@localhost//'

# List of modules to import when celery starts.
CELERY_IMPORTS = ('Databases.Users.Workers.Registration.tasks',)

# Using the rpc to store task state and results.
CELERY_RESULT_BACKEND = 'rpc://'

# Serializing and receiving only JSON.
CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'

CELERY_DEFAULT_QUEUE = 'registration'
CELERY_QUEUES = (
    Queue('registration', Exchange('registration'), routing_key='registration'),
)
