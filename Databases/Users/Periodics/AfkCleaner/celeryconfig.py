from datetime import timedelta

from kombu import Exchange, Queue

CELERYBEAT_SCHEDULE = {
    'clean_afk': {
        'task': 'Databases.Users.Workers.AfkCleaner.tasks.clean_afk_users',
        'schedule': timedelta(seconds=10)  # ,
        # 'args': ()
    },
}

# Serializing and receiving only JSON.
CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'

CELERY_TIMEZONE = 'UTC'

# Broker settings.
BROKER_URL = 'amqp://guest:guest@192.168.99.100:32778//'

CELERY_DEFAULT_QUEUE = 'afk_cleaner'
CELERY_QUEUES = (
    Queue('afk_cleaner', Exchange('afk_cleaner'), routing_key='afk_cleaner'),
)
