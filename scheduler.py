"""CPU scheduling algorithms and performance metrics.
Priority: smaller number means higher priority. SJF/Priority are non-preemptive.
"""
from collections import deque

def _validate_processes(processes):
    if not processes: raise ValueError("At least one process is required.")
    required={"pid","arrival","burst","priority"}; seen=set()
    for p in processes:
        if not required.issubset(p): raise ValueError("Each process needs pid, arrival, burst and priority.")
        pid=str(p["pid"]).strip(); arrival=int(p["arrival"]); burst=int(p["burst"]); int(p["priority"])
        if not pid: raise ValueError("Process ID cannot be empty.")
        if pid in seen: raise ValueError(f"Duplicate process ID: {pid}")
        seen.add(pid)
        if arrival<0: raise ValueError("Arrival time must be >= 0.")
        if burst<=0: raise ValueError("Burst time must be > 0.")

def _normalize(processes):
    return [{"pid":str(p["pid"]),"arrival":int(p["arrival"]),"burst":int(p["burst"]),"priority":int(p["priority"])} for p in processes]

def _finalize(processes,completion):
    rows=[]
    for p in _normalize(processes):
        ct=completion[p["pid"]]; tat=ct-p["arrival"]; wt=tat-p["burst"]
        rows.append({**p,"completion":ct,"turnaround":tat,"waiting":wt})
    rows.sort(key=lambda r:r["pid"])
    return {"processes":rows,"avg_waiting":sum(r["waiting"] for r in rows)/len(rows),"avg_turnaround":sum(r["turnaround"] for r in rows)/len(rows)}

def _result(name,processes,completion,gantt): return {"algorithm":name,"gantt":gantt,**_finalize(processes,completion)}

def _append(gantt,pid,start,end):
    if end<=start:return
    if gantt and gantt[-1][0]==pid and gantt[-1][2]==start:gantt[-1]=(pid,gantt[-1][1],end)
    else:gantt.append((pid,start,end))

def fcfs(processes):
    _validate_processes(processes); ps=sorted(_normalize(processes),key=lambda p:(p["arrival"],p["pid"])); time=0; completion={}; gantt=[]
    for p in ps:
        if time<p["arrival"]:_append(gantt,"IDLE",time,p["arrival"]); time=p["arrival"]
        start=time; time+=p["burst"]; _append(gantt,p["pid"],start,time); completion[p["pid"]]=time
    return _result("FCFS",processes,completion,gantt)

def sjf(processes):
    _validate_processes(processes); remaining=sorted(_normalize(processes),key=lambda p:(p["arrival"],p["pid"])); time=0; completion={}; gantt=[]
    while remaining:
        available=[p for p in remaining if p["arrival"]<=time]
        if not available:
            nxt=remaining[0]["arrival"]; _append(gantt,"IDLE",time,nxt); time=nxt; continue
        p=min(available,key=lambda x:(x["burst"],x["arrival"],x["pid"])); remaining.remove(p); start=time; time+=p["burst"]; _append(gantt,p["pid"],start,time); completion[p["pid"]]=time
    return _result("SJF",processes,completion,gantt)

def priority_scheduling(processes):
    _validate_processes(processes); remaining=sorted(_normalize(processes),key=lambda p:(p["arrival"],p["pid"])); time=0; completion={}; gantt=[]
    while remaining:
        available=[p for p in remaining if p["arrival"]<=time]
        if not available:
            nxt=remaining[0]["arrival"]; _append(gantt,"IDLE",time,nxt); time=nxt; continue
        p=min(available,key=lambda x:(x["priority"],x["arrival"],x["pid"])); remaining.remove(p); start=time; time+=p["burst"]; _append(gantt,p["pid"],start,time); completion[p["pid"]]=time
    return _result("Priority",processes,completion,gantt)

def round_robin(processes,quantum):
    _validate_processes(processes); quantum=int(quantum)
    if quantum<=0: raise ValueError("Round Robin time quantum must be greater than 0.")
    ps=sorted(_normalize(processes),key=lambda p:(p["arrival"],p["pid"])); remaining={p["pid"]:p["burst"] for p in ps}; completion={}; gantt=[]; q=deque(); i=0; time=0
    while i<len(ps) or q:
        if not q:
            if time<ps[i]["arrival"]:_append(gantt,"IDLE",time,ps[i]["arrival"]); time=ps[i]["arrival"]
            while i<len(ps) and ps[i]["arrival"]<=time:q.append(ps[i]["pid"]); i+=1
        pid=q.popleft(); run=min(quantum,remaining[pid]); start=time; time+=run; remaining[pid]-=run; _append(gantt,pid,start,time)
        while i<len(ps) and ps[i]["arrival"]<=time:q.append(ps[i]["pid"]); i+=1
        if remaining[pid]>0:q.append(pid)
        else:completion[pid]=time
    return _result("Round Robin",processes,completion,gantt)

def simulate_all(processes,quantum=2): return [fcfs(processes),sjf(processes),round_robin(processes,quantum),priority_scheduling(processes)]
def best_algorithm(results): return min(results,key=lambda r:(r["avg_waiting"],r["avg_turnaround"]))
def summary_rows(results): return [{"Algorithm":r["algorithm"],"Average Waiting Time":round(r["avg_waiting"],2),"Average Turnaround Time":round(r["avg_turnaround"],2)} for r in results]