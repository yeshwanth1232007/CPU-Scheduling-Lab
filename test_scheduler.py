from scheduler import fcfs,sjf,priority_scheduling,round_robin,simulate_all,best_algorithm
P=[{"pid":"P1","arrival":0,"burst":5,"priority":2},{"pid":"P2","arrival":1,"burst":3,"priority":1},{"pid":"P3","arrival":2,"burst":8,"priority":3},{"pid":"P4","arrival":3,"burst":2,"priority":2}]
def test_fcfs():
 r=fcfs(P); assert r["gantt"]==[("P1",0,5),("P2",5,8),("P3",8,16),("P4",16,18)]
def test_sjf(): assert [x[0] for x in sjf(P)["gantt"]]==["P1","P4","P2","P3"]
def test_priority(): assert [x[0] for x in priority_scheduling(P)["gantt"]]==["P1","P2","P4","P3"]
def test_rr(): assert set(x[0] for x in round_robin(P,2)["gantt"])=={"P1","P2","P3","P4"}
def test_idle():
 ps=[{"pid":"P1","arrival":0,"burst":3,"priority":1},{"pid":"P2","arrival":7,"burst":4,"priority":2}]
 for fn in (fcfs,sjf,priority_scheduling): assert ("IDLE",3,7) in fn(ps)["gantt"]
 assert ("IDLE",3,7) in round_robin(ps,2)["gantt"]
def test_validation():
 try: fcfs([{"pid":"P1","arrival":0,"burst":0,"priority":1}]); assert False
 except ValueError: assert True
def test_all(): assert len(simulate_all(P,2))==4 and best_algorithm(simulate_all(P,2))["algorithm"] in {"FCFS","SJF","Round Robin","Priority"}