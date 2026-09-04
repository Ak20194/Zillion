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
        /* ---- Nuclear option: force navy text on EVERYTHING inside the
           app first, then carve out specific exceptions after. This is
           deliberately broad because Streamlit's own text elements don't
           reliably match a fixed list of tag/testid selectors across
           versions — targeting individual tags left many elements
           (especially inside div-wrapped containers) still inheriting
           Streamlit's own theme color, which is invisible on our light
           background. Order matters below: broad rule first, narrower
           overrides after, so the later rules win on equal specificity. */
        .stApp, .stApp * {{
            color: {NAVY} !important;
        }}
        .stApp {{ background-color: {BG}; }}
        header[data-testid="stHeader"] {{ background-color: {BG}; }}
        section[data-testid="stSidebar"] {{ background-color: {CARD}; }}

        h1, h2, h3, h4 {{ font-family: Georgia, serif; }}

        /* Captions and secondary text: lighter than headings */
        [data-testid="stCaptionContainer"], [data-testid="stCaptionContainer"] * {{
            color: {NEUTRAL} !important;
        }}

        /* Brand tag: gold text on a navy pill — must come after the
           blanket rule above to win */
        .zillions-tag, .zillions-tag * {{
            color: {GOLD} !important;
        }}
        .zillions-tag {{
            display: inline-block;
            background-color: {NAVY};
            padding: 4px 14px;
            border-radius: 999px;
            font-size: 0.8rem;
            font-weight: 600;
            letter-spacing: 0.03em;
            margin-bottom: 0.5rem;
        }}

        /* Metric cards */
        div[data-testid="stMetric"] {{
            background-color: {CARD};
            border: 1px solid {GRID};
            border-radius: 10px;
            padding: 12px 16px;
        }}
        div[data-testid="stMetric"] [data-testid="stMetricLabel"],
        div[data-testid="stMetric"] [data-testid="stMetricLabel"] * {{
            color: {NEUTRAL} !important;
        }}
        div[data-testid="stMetric"] [data-testid="stMetricValue"],
        div[data-testid="stMetric"] [data-testid="stMetricValue"] * {{
            color: {NAVY} !important;
        }}
        /* Delta arrows keep their functional green/amber meaning —
           Streamlit adds its own up/down color via a data attribute;
           we only recolor the "up" (positive) case to our teal since
           amber is already close to Streamlit's native down-color. */
        div[data-testid="stMetric"] [data-testid="stMetricDelta"] svg[style*="rgb(9, 171, 59)"] {{
            fill: {POSITIVE} !important;
        }}

        /* Sliders: replace Streamlit's default red accent with our gold */
        div[data-testid="stSlider"] [role="slider"] {{
            background-color: {GOLD} !important;
            border-color: {GOLD} !important;
        }}
        div[data-testid="stSliderTickBarMin"], div[data-testid="stSliderTickBarMax"],
        div[data-testid="stSliderTickBarMin"] *, div[data-testid="stSliderTickBarMax"] * {{
            color: {NEUTRAL} !important;
        }}
        div[data-baseweb="slider"] div[data-testid="stTickBar"] {{ background: {GRID} !important; }}

        /* Buttons, links, expanders: keep readable against our light bg */
        a, a * {{ color: {GOLD} !important; }}
        summary, summary * {{ color: {NAVY} !important; }}
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
