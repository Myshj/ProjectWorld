from celery import Celery

app = Celery()
app.config_from_object('Databases.Users.Periodics.AfkCleaner.celeryconfig')
