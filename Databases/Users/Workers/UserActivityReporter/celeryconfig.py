from kombu import Queue, Exchange

# Broker settings.
BROKER_URL = 'amqp://guest:guest@192.168.99.100:32778//'

# List of modules to import when celery starts.
CELERY_IMPORTS = ('Databases.Users.Workers.UserActivityReporter.tasks',)

# Using the rpc to store task state and results.
CELERY_RESULT_BACKEND = 'rpc://'

# Serializing and receiving only JSON.
CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'

CELERY_DEFAULT_QUEUE = 'user_activity'
CELERY_QUEUES = (
    Queue('user_activity', Exchange('user_activity'), routing_key='user_activity'),
)
