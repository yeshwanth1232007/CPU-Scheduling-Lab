# ⚙️ CPU Scheduling Lab

Interactive CPU Scheduling Algorithm Simulator for an Operating Systems hackathon project.

## Problem
Traditional FCFS, SJF, Round Robin and Priority scheduling are often studied through static examples. This makes execution order and performance trade-offs difficult to visualize.

## Solution
CPU Scheduling Lab accepts process arrival time, burst time, priority and a Round Robin quantum. It runs four scheduling policies on the same workload, generates Gantt charts, calculates completion/waiting/turnaround metrics, compares averages and recommends the policy with the lowest average waiting time.

## Features
- FCFS
- Non-preemptive SJF
- Round Robin with configurable quantum
- Non-preemptive Priority
- CPU idle-time handling
- Gantt charts
- Comparison table and chart
- Process-level metrics
- Best-algorithm recommendation
- Demo presets
- CSV export
- Automated tests

## Run
```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

## Test
```bash
pytest -q
```

## Formulas
- Turnaround Time = Completion Time - Arrival Time
- Waiting Time = Turnaround Time - Burst Time

Priority convention: smaller number means higher priority.

## Structure
```text
CPU-Scheduling-Lab/
├── app.py
├── scheduler.py
├── visualization.py
├── test_scheduler.py
├── run_demo.py
├── sample_input.csv
├── requirements.txt
├── DEMO_SCRIPT.md
└── PROJECT_BRIEF.md
```

## Hackathon demo
Load **Hackathon Demo**, run it, compare all four Gantt charts and metrics, then show the recommendation. Use **CPU Idle Demo** to demonstrate arrival gaps.
