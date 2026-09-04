# The Fresh Connection — Team Zillions (#2) Dashboard

A Streamlit dashboard visualizing Team Zillions' Round 0-6 performance in
The Fresh Connection simulation: functional KPIs for Purchasing, Sales,
Supply Chain, and Operations, each linked to the financial KPIs (ROI,
Realized Revenue, COGS, Indirect Cost).

## What's inside

```
tfc_dashboard/
├── app.py                      # Executive Overview (home page)
├── pages/
│   ├── 1_VP_Purchasing.py
│   ├── 2_VP_Sales.py
│   ├── 3_VP_Supply_Chain.py
│   └── 4_VP_Operations.py
├── utils.py                    # Shared theme, colors, data loader
├── data/                       # Pre-processed CSVs (Rounds 0-6)
│   ├── financial_kpis.csv
│   ├── supplier_purchase.csv
│   ├── customer_bonus.csv
│   ├── customer_revenue.csv
│   ├── component.csv
│   ├── product.csv
│   ├── customer_product.csv
│   ├── warehouse.csv
│   └── bottling.csv
├── build_dataset.py            # Script that produced the CSVs (reference only —
│                                  not needed to run the app, source Excel files
│                                  are not included)
├── requirements.txt
└── .streamlit/config.toml      # Team Zillions color theme
```

The app reads only the CSVs in `data/` at runtime — it does **not** need the
original TFC export files or the finance report to run.

## Deploying: GitHub → Streamlit Community Cloud

1. **Create a new GitHub repository** (public or private) and push the
   entire contents of this folder to it, keeping the folder structure
   exactly as-is — `app.py` and `pages/` must be at the repo root.

   ```bash
   git init
   git add .
   git commit -m "Initial commit: Fresh Connection dashboard"
   git branch -M main
   git remote add origin https://github.com/<your-username>/<your-repo>.git
   git push -u origin main
   ```

2. **Go to [share.streamlit.io](https://share.streamlit.io)** and sign in
   with GitHub.

3. Click **"New app"**, select your repository, branch (`main`), and set
   the **main file path** to `app.py`.

4. Click **Deploy**. Streamlit Cloud will install everything listed in
   `requirements.txt` automatically — no extra configuration needed.

5. The app will be live at a URL like
   `https://<your-app-name>.streamlit.app` within a minute or two.

## Running locally (optional, to preview before deploying)

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Updating the data for a later round

If you play additional rounds and want to refresh the dashboard:

1. Export the new round's data from TFC in the same multi-sheet format
   used throughout the game, and update your finance report export.
2. Edit the file paths at the top of `build_dataset.py` to point to the
   new files, then run it locally: `python3 build_dataset.py`.
3. Commit and push the updated CSVs in `data/` — Streamlit Cloud will
   redeploy automatically on every push to the connected branch.

## Notes on data coverage

- **Rounds 0-6** are fully covered for every functional and financial KPI.
- Round 0 has no "actual" operational results for metrics like Service
  Level, MAPE, or Production Plan Adherence, since no round had been played
  yet — those fields are genuinely empty for Round 0 by design, not missing
  data.
- All figures are sourced directly from the TFC platform's own exports and
  the team's finance report; nothing in the dashboard is manually estimated.
