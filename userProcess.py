class UserProcess:
    timeSpentInCPU: int = 0
    timeLeftToFinish: int = 0

    def __init__(self, arrivalTime, burstTime):
        self.arrivalTime = arrivalTime
        self.burstTime = burstTime

    def getTimeSpentInCPU(self) -> int:
        return self.timeSpentInCPU

    def getTimeLeftToFinish(self) -> int:
        return self.timeLeftToFinish
