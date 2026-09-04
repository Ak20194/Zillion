import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from utils import (
    inject_css, team_tag, load_data, round_range_slider, filter_rounds,
    pct, money, NAVY, GOLD, POSITIVE, NEGATIVE, NEUTRAL, GRID, CARD,
    PLOTLY_TEMPLATE,
)

st.set_page_config(page_title="VP Supply Chain — Team Zillions", page_icon="🔗", layout="wide")
inject_css()
data = load_data()
team_tag()
st.title("VP Supply Chain")
st.caption(
    "Functional KPIs: Component Availability · Product Availability (OSA)  —  "
    "components and products ranked by their impact on ROI."
)

rng = round_range_slider(key="scm_rng", default=(0, 6))
comp = filter_rounds(data["component"], "round", rng)
prod = filter_rounds(data["product"], "round", rng)
fin = filter_rounds(data["financial"], "round", rng)
sup_purch = filter_rounds(data["supplier_purchase"], "round", rng)

# ---------------- Component availability ----------------
st.subheader("Component Availability")
components = sorted(comp["component"].dropna().unique())
fig = go.Figure()
for cname in components:
    sub = comp[comp["component"] == cname].sort_values("round")
    fig.add_trace(go.Scatter(x=sub["round"], y=sub["component_availability"] * 100,
                              mode="lines+markers", name=cname))
fig.update_layout(**PLOTLY_TEMPLATE["layout"].to_plotly_json())
fig.update_layout(height=380, yaxis_title="Component availability (%)", xaxis_title="Round",
                   xaxis=dict(tickmode="linear", dtick=1))
st.plotly_chart(fig, width='stretch', theme=None)

st.markdown("---")

# ---------------- Product availability (OSA) ----------------
st.subheader("Product Availability (OSA)")
products = sorted(prod["product"].dropna().unique())
fig2 = go.Figure()
for p in products:
    sub = prod[prod["product"] == p].sort_values("round")
    fig2.add_trace(go.Scatter(x=sub["round"], y=sub["osa"] * 100, mode="lines+markers", name=p))
fig2.update_layout(**PLOTLY_TEMPLATE["layout"].to_plotly_json())
fig2.update_layout(height=380, yaxis_title="OSA (%)", xaxis_title="Round",
                    xaxis=dict(tickmode="linear", dtick=1))
st.plotly_chart(fig2, width='stretch', theme=None)

st.markdown("---")

# ---------------- Component / product ranked by ROI impact ----------------
st.subheader("Components Ranked by Financial Footprint (latest round in range)")
latest_round = sup_purch["round"].max()
latest_purch = sup_purch[sup_purch["round"] == latest_round].sort_values("value", ascending=False)
fig3 = go.Figure(go.Bar(
    x=latest_purch["value"], y=latest_purch["supplier"], orientation="h",
    marker_color=GOLD,
))
fig3.update_layout(**PLOTLY_TEMPLATE["layout"].to_plotly_json())
fig3.update_layout(height=340, xaxis_title="Purchase value (€)", yaxis_title="")
st.plotly_chart(fig3, width='stretch', theme=None)
st.caption(
    "PET and Orange are the largest financial footprint components by purchase value — "
    "reliability issues here have outsized ROI impact. Vitamin C is financially immaterial "
    "despite its reliability history."
)

st.markdown("---")

st.subheader("Products Ranked by Obsolescence Risk (latest round in range)")
prod_latest_round = prod["round"].max()
prod_latest = prod[prod["round"] == prod_latest_round].sort_values("obsolete_pct", ascending=False)
fig4 = go.Figure(go.Bar(
    x=prod_latest["obsolete_pct"] * 100, y=prod_latest["product"], orientation="h",
    marker_color=NEGATIVE,
))
fig4.update_layout(**PLOTLY_TEMPLATE["layout"].to_plotly_json())
fig4.update_layout(height=340, xaxis_title="Obsolescence (%)", yaxis_title="")
st.plotly_chart(fig4, width='stretch', theme=None)

with st.expander("Underlying component data"):
    st.dataframe(comp, width='stretch')
with st.expander("Underlying product data"):
    st.dataframe(prod, width='stretch')
