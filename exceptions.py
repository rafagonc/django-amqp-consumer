

class CannotFindQueueException(Exception):

    def __init__(self, queue_name):
        self.queue_name = queue_name

    def __str__(self):
        return "Cannot find queue: " + self.queue_name + " on django settings"
