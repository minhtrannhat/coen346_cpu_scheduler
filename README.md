# COEN346 CPU Scheduler Simulation

A Priority Based Process Scheduling Simulation

## Problem Statement

- Scheduler has two queues: active and expired
- Processes are considers and scheduled for execution from the active queue.
- A Process will have:
  - PID
  - Arrival Time
  - Burst Time
  - Priority
- Priorities are between 1 and 139.
- Scheduler start at second 1 (1000ms). It assigns to the first process in the active queue its time slot and gives it the CPU. Once the time slow expires, this process is moved to the expired queue. Time slots are calculated as follows:
  - If priority < 100: `Ts = (140-priority) * 20 (millisecond)`
  - If priority >= 100: `Ts = (140-priority) * 5(millisecond)`
- When a new process arrives, its PID is inserted in the Expired Queue. _The Expired Queue is arranged in an increasing order of process priorities_.
- The scheduler' logic is basically a cycle of two activities.
  - Execute the processes in the queue flagged as active.
  - If the queue flagged as active is empty, change the flags of both queues and go back to 1.
- The scheduler updates the priority of any process that has been granted two time slots.
  - `waiting_time = sum_of_waiting_times`
  - `bonus = floor([10 * waiting_time / (now - arrival_time)])`
  - `new_priority = max(100,min(old_priority - bonus + 5,139))`
- Time unit for this program is in milliseconds but we may assume we have to update the status every 100ms. For reference, 1000ms = 1 second.
- If a process finishes running before it's time slice, the scheduler will idle till the next time slice.
- Don't create more "process" threads than necessary. Threads should be started, suspended, resumed and then joined.
- Use a min heap for the expired queue. Don't need to sort the active queue.
- Computing bonus priority should be done in userProcess.

## Implementation

- [ ] Create a parser to parse the `input.txt` file.
- [ ] Create three separate kinds of threads for: scheduler, processes and clock.
  - [ ] The scheduler only knows the PID, priority of a process and when to allocate CPU to a process. Processes from the scheduler's POV is `schedulerProcess.py`
  - [ ] A process only knows the arrival time, burst time and time spent in CPU and how much time left to finish execution. Processes from the processes itself POV is `userProcess.py`
    - The process thread is started when the CPU gives it execution time for the first time. Then it can be suspended.
  - [ ] The clock thread should be started in the main python thread.
    - [ ] Use shared Mutex and Singleton (?), use Barrier of 1 to achieve Round Robin.
