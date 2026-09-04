"""
Shared theme, colors, and helper functions used across every page of the
Team Zillions (#2) Fresh Connection dashboard.
"""
import os
from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Resolve the data/ folder relative to this file's location, not the process's
# current working directory. Streamlit Cloud does not guarantee CWD == the
# app's own folder (this varies by how the app is launched and by page
# navigation), so a bare relative path like "data/foo.csv" can fail with
# FileNotFoundError even though the file is committed and present.
DATA_DIR = Path(__file__).resolve().parent / "data"

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
    try:
        d = {}
        d["financial"] = pd.read_csv(DATA_DIR / "financial_kpis.csv")
        d["supplier_purchase"] = pd.read_csv(DATA_DIR / "supplier_purchase.csv")
        d["customer_bonus"] = pd.read_csv(DATA_DIR / "customer_bonus.csv")
        d["customer_revenue"] = pd.read_csv(DATA_DIR / "customer_revenue.csv")
        d["component"] = pd.read_csv(DATA_DIR / "component.csv")
        d["product"] = pd.read_csv(DATA_DIR / "product.csv")
        d["customer_product"] = pd.read_csv(DATA_DIR / "customer_product.csv")
        d["warehouse"] = pd.read_csv(DATA_DIR / "warehouse.csv")
        d["bottling"] = pd.read_csv(DATA_DIR / "bottling.csv")
        return d
    except FileNotFoundError as e:
        st.error(
            f"Could not find a required data file: **{e.filename}**\n\n"
            f"Looked in: `{DATA_DIR}`\n\n"
            "This usually means the `data/` folder wasn't pushed to GitHub, "
            "or a file inside it is named differently than expected "
            "(GitHub paths are case-sensitive, even if your local machine "
            "isn't). Check that your repo has a `data/` folder at the same "
            "level as `app.py`, containing all 9 CSVs listed in the README."
        )
        st.stop()


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
