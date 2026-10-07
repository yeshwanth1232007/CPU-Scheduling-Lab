from scheduler import simulate_all,best_algorithm,summary_rows
P=[{"pid":"P1","arrival":0,"burst":8,"priority":2},{"pid":"P2","arrival":1,"burst":4,"priority":1},{"pid":"P3","arrival":2,"burst":2,"priority":3},{"pid":"P4","arrival":3,"burst":5,"priority":2}]
results=simulate_all(P,2)
for row in summary_rows(results): print(f'{row["Algorithm"]:12} Avg WT={row["Average Waiting Time"]:6.2f} Avg TAT={row["Average Turnaround Time"]:6.2f}')
b=best_algorithm(results); print(f'Recommended: {b["algorithm"]}')