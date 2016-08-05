from datetime import datetime


class CommandProcessor(object):
    def __init__(self, db, logout_sender, config):
        self._db = db
        self._logout_sender = logout_sender
        self._config = config

    def clean_afk_users(self):
        """
        Logs out users that are AFK.
        """
        try:
            result = self._db.users.find({'online': True,
                                          'last_activity': {
                                              '$lt': (datetime.utcnow() - self._config.MAX_INACTIVITY_PERIOD)}})
            for document in result:
                self._logout_sender.publish_message({
                    'action': 'logout',
                    'login': document['login'],
                    'password': document['password']
                })
        except:
            pass

    def do_command(self, command):
        """
        Performs command described in dictionary.
        :param dict command: Command to perform.
        :return:
        """
        try:
            if command['action'] == 'clean_afk_users':
                self.clean_afk_users()
        except:
            pass
