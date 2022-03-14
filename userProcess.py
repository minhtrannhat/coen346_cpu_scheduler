class UserProcess:
    def __init__(self, arrivalTime, burstTime):
        self.arrivalTime = arrivalTime
        self.burstTime = burstTime
        self.timeSpentInCPU: int = 0
        self.timeLeftToFinish: int = burstTime

    def getTimeSpentInCPU(self) -> int:
        return self.timeSpentInCPU

    def getTimeLeftToFinish(self) -> int:
        return self.timeLeftToFinish
