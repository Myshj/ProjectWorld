class CommandProcessor(object):
    def __init__(self, db, user_activity_reports_sender, authorization_events_sender):
        self._db = db
        self._user_activity_reports_sender = user_activity_reports_sender
        self._authorization_events_sender = authorization_events_sender

    def login_user(self, login, password):
        """
        Tries to log user in.
        :param str login: User's login.
        :param str password: User's password.
        :return None.
        """
        try:
            self.report_user_activity(login, password)
            result = self._db.users.update_one({'login': login, 'password': password},
                                               {'$set': {'online': True}})
            self.report_login_event(login, password, result)
        except:
            pass

    def report_login_event(self, login, password, result):
        message = None
        if result.matched_count == 1:
            if result.modified_count == 1:
                message = {
                    'event': 'user_logged_in_successfully',
                    'login': login,
                    'password': password
                }
            elif result.modified_count == 0:
                message = {
                    'event': 'user_tried_to_login_but_is_already_online',
                    'login': login,
                    'password': password
                }
        elif result.matched_count == 0:
            message = {
                'event': 'user_tried_to_login_with_invalid_credentials',
                'login': login,
                'password': password
            }
        else:
            message = message = {
                'event': 'unknown_login_error',
                'login': login,
                'password': password
            }
        self._authorization_events_sender.publish_message(message)

    def logout_user(self, login, password):
        """
        Tries to log user out.
        :param str login: User's login.
        :param str password: User's password.
        :return None.
        """
        try:
            self.report_user_activity(login, password)
            result = self._db.users.update_one({'login': login, 'password': password},
                                               {'$set': {'online': False}})
            self.report_logout_event(login, password, result)
        except:
            pass

    def report_logout_event(self, login, password, result):
        message = None
        if result.matched_count == 1:
            if result.modified_count == 1:
                message = {
                    'event': 'user_logged_out_successfully',
                    'login': login,
                    'password': password
                }
            elif result.modified_count == 0:
                message = {
                    'event': 'user_tried_to_logout_but_is_already_offline',
                    'login': login,
                    'password': password
                }
        elif result.matched_count == 0:
            message = {
                'event': 'user_tried_to_logout_with_invalid_credentials',
                'login': login,
                'password': password
            }
        else:
            message = {
                'event': 'unknown_logout_error',
                'login': login,
                'password': password
            }
        self._authorization_events_sender.publish_message(message)

    def report_user_activity(self, login, password):
        message = {
            'action': 'report_user_activity',
            'login': login,
            'password': password
        }

        self._user_activity_reports_sender.publish_message(message)

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
