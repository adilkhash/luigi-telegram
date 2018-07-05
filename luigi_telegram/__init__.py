import logging
import traceback

from luigi import Task
from luigi.event import Event
import telepot

logger = logging.getLogger(__name__)

class TelegramBot(object):

    def __init__(self, bot_token):
        self.bot = telepot.Bot(bot_token)

    def send_message(self, message, chat_id):
        self.bot.sendMessage(chat_id, message, parse_mode='Markdown')


class LuigiTelegramNotification(object):
    def __init__(self, bot_token, chat_id, failed_only=False):
        self._chat_id = chat_id
        self._failed_only = failed_only

        self._succeeded_tasks = []
        self._failed_tasks = []
        self.bot = TelegramBot(bot_token)

    def on_success(self, task):
        if not self._failed_only:
            self._succeeded_tasks.append(task)

    def on_failure(self, task, exception):
        self._failed_tasks.append((task, exception))

    def set_handlers(self):
        logger.debug('Setting up handlers')
        Task.event_handler(Event.SUCCESS)(self.on_success)
        Task.event_handler(Event.FAILURE)(self.on_failure)

    def format_failure(self, task, exception):
        return 'Task: *{}*, Status: *Failed*, Exception: ```{}```\n'.format(
            task, "".join(traceback.format_exception(type(exception), exception, exception.__traceback__)))

    def format_success(self, task):
        return 'Task *{}*, Status: *Success*\n'.format(task)

    def notify(self):
        logger.debug('Total failed tasks {}'.format(len(self._failed_tasks)))
        logger.debug('Total successful tasks {}'.format(len(self._succeeded_tasks)))

        payload = [self.format_failure(*failed) for failed in self._failed_tasks]
        if not self._failed_only:
            payload += [self.format_success(task) for task in self._succeeded_tasks]

        if payload:
            self.bot.send_message(''.join(payload), self._chat_id)

    def __enter__(self):
        self.set_handlers()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.notify()
