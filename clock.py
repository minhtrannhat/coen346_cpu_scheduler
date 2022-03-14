from threading import Thread
from time import sleep


class Clock(Thread):
    def __init__(self):
        super(Clock, self).__init__()
        self.currentTime: int = 0

    def run(self):
        while True:
            if self.currentTime == 5000:
                break

            # sleep for 50 milliseconds
            sleep(0.05)

            # increment clock by 5 milliseconds
            self.currentTime += 5

    def __str__(self) -> str:
        return str(self.currentTime)
