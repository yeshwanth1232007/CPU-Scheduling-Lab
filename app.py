import pandas as pd
import streamlit as st
from scheduler import simulate_all, best_algorithm, summary_rows
from visualization import plot_gantt, plot_comparison

st.set_page_config(page_title="CPU Scheduler Lab", page_icon="⚙️", layout="wide")

EXAMPLES = {
    "Hackathon Demo": [
        {"Process":"P1","Arrival Time":0,"Burst Time":8,"Priority":2},
        {"Process":"P2","Arrival Time":1,"Burst Time":4,"Priority":1},
        {"Process":"P3","Arrival Time":2,"Burst Time":2,"Priority":3},
        {"Process":"P4","Arrival Time":3,"Burst Time":5,"Priority":2},
    ],
    "CPU Idle Demo": [
        {"Process":"P1","Arrival Time":0,"Burst Time":3,"Priority":1},
        {"Process":"P2","Arrival Time":7,"Burst Time":4,"Priority":2},
        {"Process":"P3","Arrival Time":9,"Burst Time":2,"Priority":1},
    ],
    "Round Robin Demo": [
        {"Process":"P1","Arrival Time":0,"Burst Time":5,"Priority":1},
        {"Process":"P2","Arrival Time":0,"Burst Time":4,"Priority":2},
        {"Process":"P3","Arrival Time":0,"Burst Time":3,"Priority":3},
    ],
}

st.markdown("""
<style>
.block-container{padding-top:1.4rem;max-width:1400px}
.hero{padding:1.3rem 1.5rem;border-radius:18px;border:1px solid rgba(128,128,128,.25);margin-bottom:1rem}
.hero h1{margin:0}.muted{opacity:.72}.card{padding:1rem;border:1px solid rgba(128,128,128,.22);border-radius:14px}
</style>
""", unsafe_allow_html=True)

if "input_df" not in st.session_state:
    st.session_state.input_df = pd.DataFrame(EXAMPLES["Hackathon Demo"])
if "results" not in st.session_state:
    st.session_state.results = None

st.markdown('<div class="hero"><h1>⚙️ CPU Scheduling Lab</h1><p class="muted">Interactive Operating Systems simulator — visualize, compare and learn.</p></div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("Simulation Controls")
    preset = st.selectbox("Demo scenario", ["Custom", *EXAMPLES])
    if preset != "Custom" and st.button("Load Scenario", use_container_width=True):
        st.session_state.input_df = pd.DataFrame(EXAMPLES[preset]); st.session_state.results = None; st.rerun()
    quantum = st.number_input("Round Robin Time Quantum", min_value=1, max_value=100, value=2)
    st.info("Priority rule: smaller number = higher priority.")
    st.markdown("**Algorithms**\n\n• FCFS\n• Non-preemptive SJF\n• Round Robin\n• Non-preemptive Priority")

st.subheader("1. Process Input")
edited = st.data_editor(st.session_state.input_df, num_rows="dynamic", use_container_width=True, hide_index=True,
    column_config={
        "Process": st.column_config.TextColumn("Process"),
        "Arrival Time": st.column_config.NumberColumn("Arrival Time", min_value=0, step=1),
        "Burst Time": st.column_config.NumberColumn("Burst Time", min_value=1, step=1),
        "Priority": st.column_config.NumberColumn("Priority", min_value=1, step=1),
    })
st.session_state.input_df = edited

c1,c2,c3=st.columns([2,1,1])
with c1: run=st.button("🚀 RUN SIMULATION", type="primary", use_container_width=True)
with c2:
    if st.button("↻ Reset", use_container_width=True): st.session_state.input_df=pd.DataFrame(EXAMPLES["Hackathon Demo"]); st.session_state.results=None; st.rerun()
with c3:
    if st.session_state.results:
        csv=pd.DataFrame(summary_rows(st.session_state.results)).to_csv(index=False).encode()
        st.download_button("⬇️ Results CSV", csv, "scheduling_comparison.csv", "text/csv", use_container_width=True)

if run:
    try:
        processes=[]
        for _,row in edited.iterrows():
            pid=str(row["Process"]).strip()
            if not pid or pid.lower()=="nan": raise ValueError("Every process needs a Process ID.")
            processes.append({"pid":pid,"arrival":int(row["Arrival Time"]),"burst":int(row["Burst Time"]),"priority":int(row["Priority"])})
        st.session_state.results=simulate_all(processes,int(quantum))
    except Exception as exc:
        st.error(f"Input error: {exc}"); st.session_state.results=None

results=st.session_state.results
if results:
    st.divider(); st.subheader("2. Gantt Charts")
    cols=st.columns(2)
    for i,result in enumerate(results):
        with cols[i%2]: st.pyplot(plot_gantt(result["gantt"],result["algorithm"]), use_container_width=True)
    st.subheader("3. Performance Comparison")
    st.dataframe(pd.DataFrame(summary_rows(results)), use_container_width=True, hide_index=True)
    st.pyplot(plot_comparison(results), use_container_width=True)
    best=best_algorithm(results)
    st.success(f"🏆 Best for this workload: **{best['algorithm']}** — average waiting time **{best['avg_waiting']:.2f}** units.")
    st.subheader("4. Process-Level Metrics")
    selected=st.selectbox("Algorithm",[r["algorithm"] for r in results])
    result=next(r for r in results if r["algorithm"]==selected)
    detail=pd.DataFrame(result["processes"])[["pid","arrival","burst","priority","completion","waiting","turnaround"]]
    detail.columns=["Process","Arrival","Burst","Priority","Completion","Waiting","Turnaround"]
    st.dataframe(detail,use_container_width=True,hide_index=True)
    with st.expander("📘 Algorithm explanations"):
        st.markdown("**FCFS:** arrival order. **SJF:** shortest arrived burst first. **Round Robin:** fixed time quantum in a rotating ready queue. **Priority:** highest-priority ready process first; lower number means higher priority.")
else:
    st.info("Choose a demo scenario or enter your own processes, then click **RUN SIMULATION**.")

st.divider(); st.caption("Hackathon project • Python + Streamlit + Matplotlib + Pandas • No external dataset required")