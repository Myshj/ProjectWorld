from queue import Queue


class QueueTaskProducer(object):
    def __init__(self, queue):
        """
        Constructor.
        :param Queue queue: Queue to insert tasks.
        """
        self._queue = queue

    def insert_task(self, task):
        """
        Inserts new task to the queue.
        :param task:
        :return: None.
        """
        self._queue.put_nowait(task)
