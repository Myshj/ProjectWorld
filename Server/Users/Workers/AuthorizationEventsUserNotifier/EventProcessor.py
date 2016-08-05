from threading import Thread

from BaseClasses.AMQP.Async.Sender import Worker as amqp_sender


class EventProcessor(object):
    def __init__(self, to_users_sender_config_base):
        self._to_users_sender_config_base = to_users_sender_config_base

    def process_event(self, event):
        try:
            login = event['login']
            password = event['password']
            event_type = event['event']
            sender = self.create_new_sender(login, password)
            sender_thread = Thread(target=sender.run)
            sender_thread.start()
            if event_type == 'user_logged_in_successfully':
                EventProcessor.on_user_logged_in_successfully(sender)
            elif event_type == 'user_logged_out_successfully':
                EventProcessor.on_user_logged_out_successfully(sender)
            elif event_type == 'user_tried_to_login_but_is_already_online':
                EventProcessor.on_user_tried_to_login_but_is_already_online(sender)
            elif event_type == 'user_tried_to_logout_but_is_already_offline':
                EventProcessor.on_user_tried_to_logout_but_is_already_offline(sender)
            elif event_type == 'user_tried_to_login_with_invalid_credentials':
                EventProcessor.on_invalid_credentials(sender)
            elif event_type == 'user_tried_to_logout_with_invalid_credentials':
                EventProcessor.on_invalid_credentials(sender)
            elif event_type == 'unknown_login_error':
                EventProcessor.on_unknown_error(sender)
            elif event_type == 'unknown_logout_error':
                EventProcessor.on_unknown_error(sender)
            else:
                EventProcessor.on_unknown_error(sender)
            sender.stop()
        except:
            pass

    @staticmethod
    def on_user_logged_in_successfully(sender):
        sender.publish_message({
            'event': 'you_logged_in_successfully',
        })

    @staticmethod
    def on_user_logged_out_successfully(sender):
        sender.publish_message({
            'event': 'you_logged_out_successfully',
        })

    @staticmethod
    def on_user_tried_to_login_but_is_already_online(sender):
        sender.publish_message({
            'event': 'you_are_already_online',
        })

    @staticmethod
    def on_user_tried_to_logout_but_is_already_offline(sender):
        sender.publish_message({
            'event': 'you_are_already_offline',
        })

    @staticmethod
    def on_invalid_credentials(sender):
        sender.publish_message({
            'event': 'invalid_credentials',
        })

    @staticmethod
    def on_unknown_error(sender):
        sender.publish_message({
            'event': 'server_side_error',
        })

    def create_new_sender(self, login, password):
        to_user_sender_config = self._to_users_sender_config_base.copy()
        to_user_sender_config['queue'] = '{0}_{1}'.format(login, password)
        return amqp_sender(send_to_parameters=to_user_sender_config)
