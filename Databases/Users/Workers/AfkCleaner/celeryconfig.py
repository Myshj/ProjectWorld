from kombu import Exchange, Queue

# Broker settings.
BROKER_URL = 'amqp://guest:guest@192.168.99.100:32778//'

# List of modules to import when celery starts.
CELERY_IMPORTS = ('Databases.Users.Workers.AfkCleaner.tasks',)
# Don't use result backend.
CELERY_RESULT_BACKEND = ''

# Serializing and receiving only JSON.
CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'


CELERY_DEFAULT_QUEUE = 'afk_cleaner'
CELERY_QUEUES = (
    Queue('afk_cleaner', Exchange('afk_cleaner'), routing_key='afk_cleaner'),
)
