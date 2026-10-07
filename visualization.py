import matplotlib.pyplot as plt

def plot_gantt(gantt,title):
    fig,ax=plt.subplots(figsize=(10.5,2.7)); pids=list(dict.fromkeys(pid for pid,_,_ in gantt if pid!="IDLE")); cmap=plt.get_cmap("tab20"); colors={p:cmap(i%20) for i,p in enumerate(pids)}; colors["IDLE"]="lightgray"
    for pid,start,end in gantt:
        width=end-start; ax.barh(0,width,left=start,height=.55,color=colors[pid],edgecolor="black",linewidth=.8)
        if width>=.35: ax.text((start+end)/2,0,pid,ha="center",va="center",fontsize=9,fontweight="bold")
        ax.text(start,-.43,str(start),ha="center",va="top",fontsize=8)
    if gantt: ax.text(gantt[-1][2],-.43,str(gantt[-1][2]),ha="center",va="top",fontsize=8)
    ax.set_title(f"{title} — Gantt Chart",fontsize=13,fontweight="bold"); ax.set_yticks([]); ax.set_xlabel("CPU Time"); ax.grid(axis="x",alpha=.18); ax.spines[["top","right","left"]].set_visible(False); ax.set_ylim(-.72,.48); fig.tight_layout(); return fig

def plot_comparison(results):
    names=[r["algorithm"] for r in results]; wt=[r["avg_waiting"] for r in results]; tat=[r["avg_turnaround"] for r in results]; x=list(range(len(names))); width=.36
    fig,ax=plt.subplots(figsize=(9,4.5)); ax.bar([i-width/2 for i in x],wt,width,label="Average Waiting Time"); ax.bar([i+width/2 for i in x],tat,width,label="Average Turnaround Time"); ax.set_xticks(x,names); ax.set_ylabel("Time Units"); ax.set_title("Algorithm Performance Comparison",fontweight="bold"); ax.legend(); ax.grid(axis="y",alpha=.18); fig.tight_layout(); return fig