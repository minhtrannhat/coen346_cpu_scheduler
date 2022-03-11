from threading import Thread
from time import sleep


class Clock(Thread):
    def __init__(self):
        super(Clock, self).__init__()
        self.currentTime: int = 0

    def run(self):
        while True:
            # sleep for 50 milliseconds
            sleep(0.05)
            # increment clock by 5 milliseconds
            self.currentTime = self.currentTime + 5
