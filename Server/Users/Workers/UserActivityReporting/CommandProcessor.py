class CommandProcessor(object):
    def __init__(self, db):
        self._db = db

    def report_user_activity(self, login, password):
        """
        Notifies that user has connection to the server.
        :param str login:
        :param str password:
        :return None.
        """
        try:
            self._db.users.update_one({'login': login, 'password': password},
                                      {'$currentDate': {'last_activity': True}})
        except:
            pass

    def do_command(self, command):
        """
        Performs command described in dictionary.
        :param dict command: Command to perform.
        :return:
        """
        try:
            if command['action'] == 'report_user_activity':
                self.report_user_activity(command['login'], command['password'])
        except:
            pass
