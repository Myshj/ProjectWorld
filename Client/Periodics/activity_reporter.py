from Databases.Users.Workers.UserActivityReporter.tasks import report_user_activity


def report_my_activity(login, password):
    report_user_activity.delay(login, password)
