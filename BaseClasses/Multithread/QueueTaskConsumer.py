from queue import Queue


class QueueTaskConsumer(object):
    def __init__(self, queue, process_task_callback):
        """
        Constructor.
        :param Queue queue: Queue to insert tasks.
        :param process_task_callback: Called when new task received.
        """
        self._queue = queue
        self._process_task_callback = process_task_callback

    def get_task(self):
        """
        Gets new task from the queue.
        :return: Task from the queue..
        """
        return self._queue.get()

    def run(self):
        while True:
            self._process_task_callback(self.get_task())
