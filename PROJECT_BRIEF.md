# CPU Scheduling Lab

An interactive OS scheduling simulator built with Python and Streamlit. It accepts arrival time, burst time, priority and Round Robin quantum; runs FCFS, non-preemptive SJF, Round Robin and non-preemptive Priority; generates Gantt charts; computes completion, waiting and turnaround time; compares policies; and recommends the lowest-average-waiting-time policy.

## Formulas
- Turnaround Time = Completion Time - Arrival Time
- Waiting Time = Turnaround Time - Burst Time

## Demo workload
P1: AT=0 BT=8 Priority=2; P2: AT=1 BT=4 Priority=1; P3: AT=2 BT=2 Priority=3; P4: AT=3 BT=5 Priority=2; RR quantum=2.
