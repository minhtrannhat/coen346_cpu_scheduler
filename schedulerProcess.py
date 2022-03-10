class SchedulerProcess:
    PID: str = ""
    priority: int = 0

    def __init__(self, pid, priority):
        self.PID = pid
        self.priority = priority

    def getPID(self) -> str:
        return self.PID

    def getPriority(self) -> int:
        return self.priority
