import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from utils import (
    inject_css, team_tag, load_data, round_range_slider, filter_rounds,
    pct, money, NAVY, GOLD, POSITIVE, NEGATIVE, NEUTRAL, GRID, CARD,
    PLOTLY_TEMPLATE,
)

st.set_page_config(page_title="VP Sales — Team Zillions", page_icon="🛒", layout="wide")
inject_css()
data = load_data()
team_tag()
st.title("VP Sales")
st.caption(
    "Functional KPIs: Product Avg. Attained Shelf Life · Product Avg. Achieved "
    "Service Level · Product Avg. Forecasting Error · Product Obsolescence %  —  "
    "linked to Realized Revenue and ROI, with customers prioritized by contribution."
)

rng = round_range_slider(key="sales_rng", default=(0, 6))
cp = filter_rounds(data["customer_product"], "round", rng)
prod = filter_rounds(data["product"], "round", rng)
bonus = filter_rounds(data["customer_bonus"], "round", rng)
revenue = filter_rounds(data["customer_revenue"], "round", rng)
fin = filter_rounds(data["financial"], "round", rng)

# ---------------- Customer prioritization ----------------
st.subheader("Customer Prioritization by ROI / Revenue Contribution")
c1, c2 = st.columns(2)
with c1:
    fig = go.Figure()
    for cust in ["Food & Groceries", "LAND Market", "Dominick's"]:
        sub = bonus[bonus["customer"] == cust].sort_values("round")
        fig.add_trace(go.Bar(x=sub["round"], y=sub["bonus_penalty"], name=cust))
    fig.update_layout(**PLOTLY_TEMPLATE["layout"].to_plotly_json())
    fig.update_layout(height=380, barmode="group", yaxis_title="Bonus / Penalty (€)",
                       xaxis_title="Round", xaxis=dict(tickmode="linear", dtick=1))
    st.plotly_chart(fig, width='stretch', theme=None)
with c2:
    fig2 = go.Figure()
    for cust in ["Food & Groceries", "LAND Market", "Dominick's"]:
        sub = revenue[revenue["customer"] == cust].sort_values("round")
        fig2.add_trace(go.Bar(x=sub["round"], y=sub["contracted_revenue"], name=cust))
    fig2.update_layout(**PLOTLY_TEMPLATE["layout"].to_plotly_json())
    fig2.update_layout(height=380, barmode="stack", yaxis_title="Contracted Revenue (€)",
                        xaxis_title="Round", xaxis=dict(tickmode="linear", dtick=1))
    st.plotly_chart(fig2, width='stretch', theme=None)

latest_round = revenue["round"].max()
latest_rev = revenue[revenue["round"] == latest_round].sort_values("contracted_revenue", ascending=False)
st.caption(
    "Customer ranking by contracted revenue (latest round in range): "
    + ", ".join(f"{r['customer']} ({money(r['contracted_revenue'])})" for _, r in latest_rev.iterrows())
)

st.markdown("---")

# ---------------- Shelf life & service level ----------------
st.subheader("Attained Shelf Life & Achieved Service Level")
c3, c4 = st.columns(2)
with c3:
    sl_by_round = cp.groupby("round")["attained_shelf_life"].mean().reset_index()
    fig3 = go.Figure(go.Scatter(x=sl_by_round["round"], y=sl_by_round["attained_shelf_life"] * 100,
                                 mode="lines+markers", line=dict(color=POSITIVE)))
    fig3.update_layout(**PLOTLY_TEMPLATE["layout"].to_plotly_json())
    fig3.update_layout(height=340, yaxis_title="Avg. attained shelf life (%)", xaxis_title="Round",
                        xaxis=dict(tickmode="linear", dtick=1))
    st.plotly_chart(fig3, width='stretch', theme=None)
with c4:
    sl2_by_round = cp.groupby("round")[["service_level_pieces", "service_level_order_lines"]].mean().reset_index()
    fig4 = go.Figure()
    fig4.add_trace(go.Scatter(x=sl2_by_round["round"], y=sl2_by_round["service_level_pieces"] * 100,
                               mode="lines+markers", name="Service level (pieces)", line=dict(color=NAVY)))
    fig4.add_trace(go.Scatter(x=sl2_by_round["round"], y=sl2_by_round["service_level_order_lines"] * 100,
                               mode="lines+markers", name="Service level (order lines)", line=dict(color=GOLD)))
    fig4.update_layout(**PLOTLY_TEMPLATE["layout"].to_plotly_json())
    fig4.update_layout(height=340, yaxis_title="Avg. service level (%)", xaxis_title="Round",
                        xaxis=dict(tickmode="linear", dtick=1))
    st.plotly_chart(fig4, width='stretch', theme=None)

st.markdown("---")

# ---------------- Forecast error & obsolescence ----------------
st.subheader("Forecast Error (MAPE) & Product Obsolescence")
c5, c6 = st.columns(2)
with c5:
    mape_by_round = prod.groupby("round")["mape"].mean().reset_index()
    fig5 = go.Figure(go.Bar(x=mape_by_round["round"], y=mape_by_round["mape"] * 100, marker_color=NEGATIVE))
    fig5.update_layout(**PLOTLY_TEMPLATE["layout"].to_plotly_json())
    fig5.update_layout(height=340, yaxis_title="Avg. MAPE (%)", xaxis_title="Round",
                        xaxis=dict(tickmode="linear", dtick=1))
    st.plotly_chart(fig5, width='stretch', theme=None)
with c6:
    products = sorted(prod["product"].dropna().unique())
    fig6 = go.Figure()
    for p in products:
        sub = prod[prod["product"] == p].sort_values("round")
        fig6.add_trace(go.Scatter(x=sub["round"], y=sub["obsolete_pct"] * 100, mode="lines+markers", name=p))
    fig6.update_layout(**PLOTLY_TEMPLATE["layout"].to_plotly_json())
    fig6.update_layout(height=340, yaxis_title="Obsolescence (%)", xaxis_title="Round",
                        xaxis=dict(tickmode="linear", dtick=1))
    st.plotly_chart(fig6, width='stretch', theme=None)
st.caption(
    "Forecast error (MAPE) stayed high (47-61%) across every round and never meaningfully "
    "improved — the single largest unresolved functional KPI gap in Sales."
)

with st.expander("Underlying customer-product data"):
    st.dataframe(cp, width='stretch')
