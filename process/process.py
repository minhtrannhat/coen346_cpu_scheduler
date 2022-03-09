#!/usr/bin/env python3


class Process:
    def __init__(self, id, arrivalTime, burst, initialPriority):
        self.id = id
        self.arrivalTime = arrivalTime
        self.burst = burst
        self.initialPriority = initialPriority
