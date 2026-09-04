import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from utils import (
    inject_css, team_tag, load_data, round_range_slider, filter_rounds,
    pct, money, NAVY, GOLD, POSITIVE, NEGATIVE, NEUTRAL, GRID, CARD,
    PLOTLY_TEMPLATE, Y2_AXIS_STYLE, axis_title,
)

st.set_page_config(page_title="VP Operations — Team Zillions", page_icon="🏭", layout="wide")
inject_css()
data = load_data()
team_tag()
st.title("VP Operations")
st.caption(
    "Functional KPIs: Inbound & Outbound Warehouse Cube Utilization · Production "
    "Plan Adherence %  —  linked to ROI and COGS."
)

rng = round_range_slider(key="ops_rng", default=(0, 6))
wh = filter_rounds(data["warehouse"], "round", rng)
prod = filter_rounds(data["product"], "round", rng)
fin = filter_rounds(data["financial"], "round", rng)

# ---------------- Warehouse cube utilization ----------------
st.subheader("Inbound (RM) & Outbound (FG) Warehouse Cube Utilization")
rm = wh[wh["warehouse"].str.contains("Raw materials", na=False)].sort_values("round")
fg = wh[wh["warehouse"].str.contains("Finished goods", na=False)].sort_values("round")

c1, c2 = st.columns(2)
with c1:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=rm["round"], y=rm["cube_utilization"] * 100,
                              mode="lines+markers", name="RM cube utilization", line=dict(color=NAVY)))
    fig.add_trace(go.Scatter(x=fg["round"], y=fg["cube_utilization"] * 100,
                              mode="lines+markers", name="FG cube utilization", line=dict(color=GOLD)))
    fig.add_hrect(y0=80, y1=90, fillcolor=POSITIVE, opacity=0.08, line_width=0)
    fig.update_layout(**PLOTLY_TEMPLATE["layout"].to_plotly_json())
    fig.update_layout(height=380, yaxis_title="Cube utilization (%)", xaxis_title="Round",
                       xaxis=dict(tickmode="linear", dtick=1))
    st.plotly_chart(fig, width='stretch', theme=None)
    st.caption("Shaded band = the ~80-90% efficient utilization range targeted across the game.")
with c2:
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(x=rm["round"], y=rm["overflow_pct"] * 100, name="RM overflow %", marker_color=NEGATIVE))
    fig2.add_trace(go.Bar(x=fg["round"], y=fg["overflow_pct"] * 100, name="FG overflow %", marker_color=GOLD))
    fig2.update_layout(**PLOTLY_TEMPLATE["layout"].to_plotly_json())
    fig2.update_layout(height=380, barmode="group", yaxis_title="Overflow (%)", xaxis_title="Round",
                        xaxis=dict(tickmode="linear", dtick=1))
    st.plotly_chart(fig2, width='stretch', theme=None)

st.caption(
    "Round 2 shows the overflow crisis (RM/FG both near-full). Round 4 overcorrects into "
    "under-utilization after the capacity increase. Round 5-6 stabilize back into range, "
    "though Round 6's RM capacity increase (1,200→1,300) landed at only ~58% utilization."
)

st.markdown("---")

# ---------------- Production plan adherence ----------------
st.subheader("Production Plan Adherence")
adh_by_round = prod.groupby("round")["production_plan_adherence"].mean().reset_index()
fig3 = go.Figure(go.Scatter(
    x=adh_by_round["round"], y=adh_by_round["production_plan_adherence"] * 100,
    mode="lines+markers", line=dict(color=POSITIVE, width=3),
))
fig3.add_hline(y=90, line_dash="dot", line_color=NEUTRAL, annotation_text="90% target")
fig3.update_layout(**PLOTLY_TEMPLATE["layout"].to_plotly_json())
fig3.update_layout(height=380, yaxis_title="Avg. production plan adherence (%)", xaxis_title="Round",
                    xaxis=dict(tickmode="linear", dtick=1))
st.plotly_chart(fig3, width='stretch', theme=None)
st.caption(
    "Adherence climbed from the low-80s to 96%+ by Round 5-6, driven by SMED, preventive "
    "maintenance, and breakdown training — the clearest operational win of the whole game."
)

st.markdown("---")

# ---------------- Cost linkage ----------------
st.subheader("Warehouse & Labor Cost, linked to COGS")
merged = fin[["round", "cogs", "production_costs"]].copy()
fig4 = go.Figure()
fig4.add_trace(go.Bar(x=merged["round"], y=merged["production_costs"], name="Production costs", marker_color=NAVY))
fig4.add_trace(go.Scatter(x=merged["round"], y=merged["cogs"], name="Total COGS", mode="lines+markers",
                           line=dict(color=GOLD), yaxis="y2"))
fig4.update_layout(**PLOTLY_TEMPLATE["layout"].to_plotly_json())
fig4.update_layout(
    height=380,
    yaxis=dict(title="Production costs (€)"),
    yaxis2=dict(title=axis_title("Total COGS (€)"), overlaying="y", side="right", showgrid=False, **Y2_AXIS_STYLE),
    xaxis=dict(title="Round", tickmode="linear", dtick=1),
)
st.plotly_chart(fig4, width='stretch', theme=None)
st.caption(
    "Round 5's third-shift decision spiked production cost (+€100k/round in permanent "
    "employees) against 37% idle bottling capacity — reversed in Round 6, recovering ~€86.5k."
)

with st.expander("Underlying warehouse data"):
    st.dataframe(wh, width='stretch')
with st.expander("Underlying bottling line data"):
    st.dataframe(data["bottling"], width='stretch')
