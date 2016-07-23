import time
from optparse import OptionParser

from Databases.Users.Workers.Login.tasks import login_user, logout_user


def login_me(login, password):
    """
    Tries to log user in.
    :param str login: User's login.
    :param str password: User's password.
    :return: True if user successfully logged in. False otherwise.
    """
    return login_user.delay(login, password).get(timeout=10)


def logout_me(login, password):
    """
    Tries to log user out.
    :param str login: User's login.
    :param str password: User's password.
    :return: True if user successfully logged out. False otherwise.
    """
    return logout_user.delay(login, password).get(timeout=10)


def do(action, login, password):
    """
    Logs user in or out.
    :param str action: 'login' or 'logout'
    :param str login: User's login.
    :param str password: User's password.
    :return: 'success' if user successfully logged in or out. 'failure' otherwise.
    """
    what_to_do = None
    if action == 'login':
        what_to_do = login_me
    elif action == 'logout':
        what_to_do = logout_me

    if what_to_do:
        if what_to_do(login, password):
            return 'success'
        else:
            return 'failure'
    else:
        return 'failure'


def clock(interval, login, password):
    from Databases.Users.Workers.UserActivityReporter.tasks import report_user_activity
    while True:
        print("The time is %s" % time.ctime())
        report_user_activity.delay(login, password)
        time.sleep(interval)


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-a", "--action",
                      action="store", type="string", dest="action")
    parser.add_option("-l", "--login",
                      action="store", type="string", dest="login")
    parser.add_option("-p", "--password",
                      action="store", type="string", dest="password")
    (options, args) = parser.parse_args()

    print(do(options.action, options.login, options.password))

    import threading

    t = threading.Thread(target=clock, args=(0.0001, options.login, options.password,))
    t.start()
