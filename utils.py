"""
Shared theme, colors, and helper functions used across every page of the
Team Zillions (#2) Fresh Connection dashboard.
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# ---------------- Team Zillions palette ----------------
BG = "#F7F3EA"          # warm ivory background
CARD = "#FFFDF8"        # soft cream card background
NAVY = "#1E2A4A"         # primary text / headers
GOLD = "#C89B3C"         # brand accent
POSITIVE = "#2F6E5B"     # forest teal - beat target / positive
NEGATIVE = "#D98E3F"     # warm amber - miss target / negative (never red)
NEUTRAL = "#6B6259"      # warm grey - secondary text
GRID = "#E8E2D6"         # chart gridlines

PLOTLY_TEMPLATE = dict(
    layout=go.Layout(
        paper_bgcolor=CARD,
        plot_bgcolor=CARD,
        font=dict(family="Georgia, serif", color=NAVY, size=13),
        colorway=[NAVY, GOLD, POSITIVE, NEGATIVE, "#8C9BD4", "#B08968"],
        xaxis=dict(gridcolor=GRID, zerolinecolor=GRID),
        yaxis=dict(gridcolor=GRID, zerolinecolor=GRID),
        legend=dict(bgcolor=CARD),
    )
)


def inject_css():
    st.markdown(
        f"""
        <style>
        .stApp {{ background-color: {BG}; }}
        section[data-testid="stSidebar"] {{ background-color: {CARD}; }}
        h1, h2, h3, h4 {{ color: {NAVY} !important; font-family: Georgia, serif; }}
        .zillions-tag {{
            display: inline-block;
            background-color: {NAVY};
            color: {GOLD};
            padding: 4px 14px;
            border-radius: 999px;
            font-size: 0.8rem;
            font-weight: 600;
            letter-spacing: 0.03em;
            margin-bottom: 0.5rem;
        }}
        div[data-testid="stMetric"] {{
            background-color: {CARD};
            border: 1px solid {GRID};
            border-radius: 10px;
            padding: 12px 16px;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def team_tag():
    st.markdown('<div class="zillions-tag">TEAM ZILLIONS · #2</div>', unsafe_allow_html=True)


@st.cache_data
def load_data():
    d = {}
    d["financial"] = pd.read_csv("data/financial_kpis.csv")
    d["supplier_purchase"] = pd.read_csv("data/supplier_purchase.csv")
    d["customer_bonus"] = pd.read_csv("data/customer_bonus.csv")
    d["customer_revenue"] = pd.read_csv("data/customer_revenue.csv")
    d["component"] = pd.read_csv("data/component.csv")
    d["product"] = pd.read_csv("data/product.csv")
    d["customer_product"] = pd.read_csv("data/customer_product.csv")
    d["warehouse"] = pd.read_csv("data/warehouse.csv")
    d["bottling"] = pd.read_csv("data/bottling.csv")
    return d


def round_range_slider(key="round_range", min_round=0, max_round=6, default=(0, 6)):
    return st.slider(
        "Round range", min_value=min_round, max_value=max_round,
        value=default, step=1, key=key,
    )


def filter_rounds(df, round_col, rng):
    return df[(df[round_col] >= rng[0]) & (df[round_col] <= rng[1])]


def pct(x, decimals=1):
    if pd.isna(x):
        return "—"
    return f"{x*100:.{decimals}f}%"


def money(x, decimals=0):
    if pd.isna(x):
        return "—"
    return f"€{x:,.{decimals}f}"


def kpi_delta_color(current, target):
    """Returns POSITIVE if current beats/meets target, else NEGATIVE."""
    if pd.isna(current) or pd.isna(target):
        return NEUTRAL
    return POSITIVE if current >= target else NEGATIVE
