import datetime


class Registrationer(object):
    def __init__(self, db):
        self._db = db

    def register_user(self, login, password, emails):
        """
        Tries to register new user.
        :param str login: Login for user.
        :param str password: Password for user.
        :param [str] emails: Emails for user.
        :return None.
        """
        try:
            self._db.users.insert_one({'login': login,
                                       'password': password,
                                       'emails': emails,
                                       'online': False,
                                       'last_activity': datetime.datetime.utcnow()})
        except:
            pass

    def remove_user(self, login, password):
        """
        Tries to remove user.
        :param str login: User's login.
        :param str password: User's password.
        :return None.
        """
        try:
            self._db.users.delete_many({'login': login, 'password': password})
        except:
            pass

    def do_command(self, command):
        """
        Performs command described in dictionary.
        :param dict command: Command to perform.
        :return:
        """
        try:
            if command['action'] == 'register_user':
                self.register_user(command['login'], command['password'], command['emails'])
            elif command['action'] == 'remove_user':
                self.remove_user(command['login'], command['password'])
        except:
            pass
