import streamlit as st
import plotly.graph_objects as go
from utils import (
    inject_css, team_tag, load_data, round_range_slider, filter_rounds,
    pct, money, NAVY, GOLD, POSITIVE, NEGATIVE, NEUTRAL, GRID, CARD,
    PLOTLY_TEMPLATE,
)

st.set_page_config(
    page_title="The Fresh Connection — Team Zillions",
    page_icon="📦",
    layout="wide",
)
inject_css()
data = load_data()
fin = data["financial"]

team_tag()
st.title("The Fresh Connection — Performance Dashboard")
st.caption(
    "Team Zillions (#2) · Round-by-round KPIs across Purchasing, Sales, "
    "Supply Chain, and Operations, linked to ROI, Realized Revenue, COGS, "
    "and Indirect Cost."
)

rng = round_range_slider(default=(0, 6))
f = filter_rounds(fin, "round", rng)

# ---------------- Top-line stat cards ----------------
c1, c2, c3, c4 = st.columns(4)
latest = f.iloc[-1]
peak = f.loc[f["roi"].idxmax()]
c1.metric("Latest ROI", pct(latest["roi"]), f"Round {int(latest['round'])}")
c2.metric("Peak ROI", pct(peak["roi"]), f"Round {int(peak['round'])}")
c3.metric("Latest Realized Revenue", money(latest["realized_revenue"]))
c4.metric("Latest Operating Profit", money(latest["operating_profit"]))

st.markdown("---")

# ---------------- ROI trajectory ----------------
left, right = st.columns([2, 1])
with left:
    st.subheader("ROI Trajectory")
    colors = [POSITIVE if v >= 0 else NEGATIVE for v in f["roi"]]
    fig = go.Figure(go.Bar(
        x=f["round"], y=f["roi"] * 100,
        marker_color=colors,
        text=[f"{v*100:.2f}%" for v in f["roi"]],
        textposition="outside",
    ))
    fig.update_layout(**PLOTLY_TEMPLATE["layout"].to_plotly_json())
    fig.update_layout(
        height=380, yaxis_title="ROI (%)", xaxis_title="Round",
        xaxis=dict(tickmode="linear", dtick=1),
    )
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("Revenue vs. Cost")
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(x=f["round"], y=f["realized_revenue"], name="Realized Revenue", marker_color=NAVY))
    fig2.add_trace(go.Bar(x=f["round"], y=f["cogs"], name="COGS", marker_color=GOLD))
    fig2.add_trace(go.Bar(x=f["round"], y=f["indirect_cost"], name="Indirect Cost", marker_color=NEGATIVE))
    fig2.update_layout(**PLOTLY_TEMPLATE["layout"].to_plotly_json())
    fig2.update_layout(height=380, barmode="group", xaxis_title="Round", yaxis_title="€",
                        xaxis=dict(tickmode="linear", dtick=1))
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# ---------------- Operating profit bridge (round over round) ----------------
st.subheader("Operating Profit — Round-over-Round Bridge")
bridge_rounds = f["round"].tolist()
if len(bridge_rounds) >= 2:
    idx = st.select_slider(
        "Compare consecutive rounds",
        options=list(range(len(bridge_rounds) - 1)),
        format_func=lambda i: f"Round {bridge_rounds[i]} → Round {bridge_rounds[i+1]}",
        value=len(bridge_rounds) - 2,
    )
    r0 = f.iloc[idx]
    r1 = f.iloc[idx + 1]
    revenue_delta = r1["realized_revenue"] - r0["realized_revenue"]
    purchase_delta = -(r1["purchase_value"] - r0["purchase_value"])
    production_delta = -(r1["production_costs"] - r0["production_costs"])
    indirect_delta = -(r1["indirect_cost"] - r0["indirect_cost"])

    fig3 = go.Figure(go.Waterfall(
        orientation="v",
        measure=["absolute", "relative", "relative", "relative", "relative", "total"],
        x=[f"Rd {int(r0['round'])} Op. Profit", "Revenue", "Purchase Cost", "Production Cost",
           "Indirect Cost", f"Rd {int(r1['round'])} Op. Profit"],
        y=[r0["operating_profit"], revenue_delta, purchase_delta, production_delta,
           indirect_delta, 0],
        connector={"line": {"color": GRID}},
        increasing={"marker": {"color": POSITIVE}},
        decreasing={"marker": {"color": NEGATIVE}},
        totals={"marker": {"color": NAVY}},
    ))
    fig3.update_layout(**PLOTLY_TEMPLATE["layout"].to_plotly_json())
    fig3.update_layout(height=420, yaxis_title="€")
    st.plotly_chart(fig3, use_container_width=True)
    st.caption(
        f"Operating profit moved from {money(r0['operating_profit'])} to "
        f"{money(r1['operating_profit'])} between Round {int(r0['round'])} and "
        f"Round {int(r1['round'])}."
    )

st.markdown("---")
st.info(
    "Use the sidebar to open the **VP Purchasing**, **VP Sales**, "
    "**VP Supply Chain**, and **VP Operations** pages — each links its "
    "functional KPIs directly to ROI, Realized Revenue, COGS, and Indirect Cost."
)
