class Loginer(object):
    def __init__(self, db, user_activity_sender):
        self._db = db
        self._user_activity_sender = user_activity_sender

    def login_user(self, login, password):
        """
        Tries to log user in.
        :param str login: User's login.
        :param str password: User's password.
        :return None.
        """
        try:
            self.report_user_activity(login, password)
            self._db.users.update_one({'login': login, 'password': password},
                                      {'$set': {'online': True}})
        except:
            pass

    def logout_user(self, login, password):
        """
        Tries to log user out.
        :param str login: User's login.
        :param str password: User's password.
        :return None.
        """
        try:
            self.report_user_activity(login, password)
            self._db.users.update_one({'login': login, 'password': password},
                                      {'$set': {'online': False}})
        except:
            pass

    def report_user_activity(self, login, password):
        message = {
            'action': 'report_user_activity',
            'login': login,
            'password': password
        }

        self._user_activity_sender.publish_message(message)

    def do_command(self, command):
        """
        Performs command described in dictionary.
        :param dict command: Command to perform.
        :return:
        """
        try:
            if command['action'] == 'login':
                self.login_user(command['login'], command['password'])
            elif command['action'] == 'logout':
                self.logout_user(command['login'], command['password'])
        except:
            pass
