from threading import Thread


class Clock(Thread):
    def __init__(self):
        super(Clock, self).__init__()
