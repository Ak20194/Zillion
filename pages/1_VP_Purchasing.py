import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from utils import (
    inject_css, team_tag, load_data, round_range_slider, filter_rounds,
    pct, money, NAVY, GOLD, POSITIVE, NEGATIVE, NEUTRAL, GRID, CARD,
    PLOTLY_TEMPLATE, Y2_AXIS_STYLE, axis_title,
)

st.set_page_config(page_title="VP Purchasing — Team Zillions", page_icon="📦", layout="wide")
inject_css()
data = load_data()
team_tag()
st.title("VP Purchasing")
st.caption(
    "Functional KPIs: Component Delivery Reliability · Component Rejection % · "
    "Component Obsolete % · Raw Material Cost %  —  linked to ROI and COGS."
)

rng = round_range_slider(key="purch_rng", default=(0, 6))
comp = filter_rounds(data["component"], "round", rng)
fin = filter_rounds(data["financial"], "round", rng)
sup_purch = filter_rounds(data["supplier_purchase"], "round", rng)

components = sorted(comp["component"].dropna().unique())

# ---------------- Delivery reliability trend ----------------
st.subheader("Component Delivery Reliability vs. Rejection %")
c1, c2 = st.columns(2)
with c1:
    fig = go.Figure()
    for i, cname in enumerate(components):
        sub = comp[comp["component"] == cname].sort_values("round")
        fig.add_trace(go.Scatter(
            x=sub["round"], y=sub["delivery_reliability"] * 100,
            mode="lines+markers", name=cname,
        ))
    fig.update_layout(**PLOTLY_TEMPLATE["layout"].to_plotly_json())
    fig.update_layout(height=380, yaxis_title="Delivery reliability (%)", xaxis_title="Round",
                       xaxis=dict(tickmode="linear", dtick=1))
    st.plotly_chart(fig, width='stretch')
with c2:
    fig2 = go.Figure()
    for i, cname in enumerate(components):
        sub = comp[comp["component"] == cname].sort_values("round")
        fig2.add_trace(go.Scatter(
            x=sub["round"], y=sub["rejection_pct"] * 100,
            mode="lines+markers", name=cname,
        ))
    fig2.update_layout(**PLOTLY_TEMPLATE["layout"].to_plotly_json())
    fig2.update_layout(height=380, yaxis_title="Rejection (%)", xaxis_title="Round",
                        xaxis=dict(tickmode="linear", dtick=1))
    st.plotly_chart(fig2, width='stretch')

st.caption(
    "PET's reliability collapsed under Trio PET PLC (Rounds 1-3, Poor quality rating) "
    "and recovered sharply after the switch to Plantin PET in Round 4. "
    "Vitamin C shows the same pattern with the Seitan → AIL Vitamins switch in Round 5."
)

st.markdown("---")

# ---------------- Component availability & obsolescence ----------------
st.subheader("Component Availability & Obsolescence")
c3, c4 = st.columns(2)
with c3:
    fig3 = go.Figure()
    for cname in components:
        sub = comp[comp["component"] == cname].sort_values("round")
        fig3.add_trace(go.Scatter(
            x=sub["round"], y=sub["component_availability"] * 100,
            mode="lines+markers", name=cname,
        ))
    fig3.update_layout(**PLOTLY_TEMPLATE["layout"].to_plotly_json())
    fig3.update_layout(height=340, yaxis_title="Component availability (%)", xaxis_title="Round",
                        xaxis=dict(tickmode="linear", dtick=1))
    st.plotly_chart(fig3, width='stretch')
with c4:
    fig4 = go.Figure()
    for cname in components:
        sub = comp[comp["component"] == cname].sort_values("round")
        fig4.add_trace(go.Bar(x=sub["round"], y=sub["obsolete_pct"] * 100, name=cname))
    fig4.update_layout(**PLOTLY_TEMPLATE["layout"].to_plotly_json())
    fig4.update_layout(height=340, yaxis_title="Obsolete (%)", xaxis_title="Round", barmode="group",
                        xaxis=dict(tickmode="linear", dtick=1))
    st.plotly_chart(fig4, width='stretch')
st.caption("Component obsolescence is 0% in every round — raw materials carry no shelf-life risk in this model.")

st.markdown("---")

# ---------------- Raw material cost % of COGS, linked to ROI ----------------
st.subheader("Raw Material Cost % of COGS — linked to ROI")
merged = fin.copy()
merged["raw_material_cost_pct"] = merged["purchase_value"] / merged["cogs"]

fig5 = go.Figure()
fig5.add_trace(go.Bar(
    x=merged["round"], y=merged["raw_material_cost_pct"] * 100,
    name="Raw material cost % of COGS", marker_color=GOLD, yaxis="y1",
))
fig5.add_trace(go.Scatter(
    x=merged["round"], y=merged["roi"] * 100,
    name="ROI (%)", mode="lines+markers", marker_color=NAVY, yaxis="y2",
))
fig5.update_layout(**PLOTLY_TEMPLATE["layout"].to_plotly_json())
fig5.update_layout(
    height=400,
    yaxis=dict(title="Raw material cost (% of COGS)"),
    yaxis2=dict(title=axis_title("ROI (%)"), overlaying="y", side="right", showgrid=False, **Y2_AXIS_STYLE),
    xaxis=dict(title="Round", tickmode="linear", dtick=1),
)
st.plotly_chart(fig5, width='stretch')
st.caption(
    "Purchase value stayed within a tight band across all 6 rounds even through 3 "
    "supplier switches — the supplier changes were quality/reliability driven, not cost-driven."
)

st.markdown("---")

# ---------------- Purchase value by supplier ----------------
st.subheader("Purchase Value by Supplier")
fig6 = go.Figure()
for sup in sorted(sup_purch["supplier"].unique()):
    sub = sup_purch[sup_purch["supplier"] == sup].sort_values("round")
    fig6.add_trace(go.Bar(x=sub["round"], y=sub["value"], name=sup))
fig6.update_layout(**PLOTLY_TEMPLATE["layout"].to_plotly_json())
fig6.update_layout(height=420, barmode="stack", yaxis_title="Purchase value (€)", xaxis_title="Round",
                    xaxis=dict(tickmode="linear", dtick=1))
st.plotly_chart(fig6, width='stretch')

with st.expander("Underlying component data"):
    st.dataframe(comp, width='stretch')
