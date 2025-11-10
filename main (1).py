
# main.py (updated)
import streamlit as st
import pandas as pd

# Try to import your helper as "preprocess"; fall back to st.* if missing.
try:
    import alphapreprocess as preprocess  # renamed helper module
except Exception:
    class _Shim:
        def multiselect(self, *args, **kwargs):
            return st.sidebar.multiselect(*args, **kwargs)
    preprocess = _Shim()

from charts import (
    plot_daily_transactions,
    plot_fraud_analysis,
    plot_distribution_of_transaction_amounts,
    plot_fraud_type_analysis,
    plot_heatmap,
    plot_crime_level_trends
)

# ---------------------------- DATA LOADING & PAGE CONFIG ----------------------------
st.set_page_config(
    page_icon="Blackmoney.png",   # updated filename (no space, lowercase m)
    page_title="Black Money Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Try multiple possible CSVs in priority order
CANDIDATE_CSVS = ["merged_data.csv", "newdataset.csv", "dataset1.csv", "MachineLearningtaging.csv"]
csv_found = None
for name in CANDIDATE_CSVS:
    try:
        df = pd.read_csv(name)
        csv_found = name
        break
    except Exception:
        continue

if csv_found is None:
    st.error("No data CSV found. Expected one of: " + ", ".join(CANDIDATE_CSVS))
    st.stop()

data = df.copy()

# Normalize column names (case/space insensitive) to expected names
import re
def normalize_columns(df):
    want = {
        "month": ["month", "mnth"],
        "typeofaction": ["typeofaction", "type_of_action", "actiontype", "transactiontype", "type"],
        "isfraud": ["isfraud", "is_fraud", "fraud", "fraud_flag"],
        "typeofcrime": ["typeofcrime", "type_of_crime", "crime_class", "crime"],
        "amountofmoney": ["amountofmoney", "amount", "transactionamount", "amt"],
        "date": ["date", "transactiondate", "datetime", "time"]
    }
    lc = {re.sub(r"[^a-z0-9]", "", c.lower()): c for c in df.columns}
    mapping = {}
    for std, alts in want.items():
        for a in alts:
            k = re.sub(r"[^a-z0-9]", "", a.lower())
            if k in lc:
                mapping[lc[k]] = std
                break
    df = df.rename(columns=mapping)
    return df

data = normalize_columns(data)

# ---------------------------- CUSTOM CSS ----------------------------
st.markdown("""
    <style>
    .main { padding: 0rem 1rem; }
    .dashboard-header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 10px; margin-bottom: 2rem; box-shadow: 0 4px 6px rgba(0,0,0,.1); }
    .dashboard-title { color: white; font-size: 2.5rem; font-weight: bold; margin: 0; text-align: center; }
    .dashboard-subtitle { color: #f0f0f0; font-size: 1rem; text-align: center; margin-top: .5rem; }
    .logo-container { text-align: center; padding: 1rem; }
    .objective-section { background: #f8f9fa; padding: 1.5rem; border-radius: 10px; border-left: 5px solid #667eea; margin: 2rem 0; box-shadow: 0 2px 4px rgba(0,0,0,.05); }
    .objective-title { color: #667eea; font-size: 1.3rem; font-weight: bold; margin-bottom: 1rem; }
    .objective-text { color: #444; line-height: 1.6; text-align: justify; }
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #667eea 0%, #764ba2 100%); }
    [data-testid="stSidebar"] .stMarkdown { color: white; }
    .metric-card { background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,.1); margin: 1rem 0; border-left: 4px solid #667eea; }
    .metric-value { font-size: 2rem; font-weight: bold; color: #667eea; }
    .metric-label { color: #666; font-size: .9rem; text-transform: uppercase; letter-spacing: 1px; }
    .footer { position: relative; bottom: 0; width: 100%; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; text-align: center; font-size: 16px; margin-top: 3rem; padding: 2rem 0; border-radius: 10px; box-shadow: 0 -2px 10px rgba(0,0,0,.1); }
    .footer a { color: #ffd700; text-decoration: none; font-weight: bold; transition: color .3s; }
    .footer a:hover { color: #ffed4e; text-decoration: underline; }
    .chart-container { background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,.1); margin: 1.5rem 0; }
    .stAlert { border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

# ---------------------------- HEADER ----------------------------
col1, col2, col3 = st.columns([1,2,1])
with col1:
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    try:
        st.image("Blackmoney.png", width=150)
    except Exception:
        st.write("")
    st.markdown('</div>', unsafe_allow_html=True)
with col2:
    st.markdown("""
        <div class="dashboard-header">
            <h1 class="dashboard-title">🔍 Black Money Dashboard</h1>
            <p class="dashboard-subtitle">Financial Crime Detection & Analysis System</p>
        </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown('<div style="padding: 2rem;"></div>', unsafe_allow_html=True)

# ---------------------------- METRICS ----------------------------
st.markdown("### 📈 Key Metrics")
metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

with metric_col1:
    total_transactions = len(data)
    st.markdown(f'''<div class="metric-card">
            <div class="metric-label">Total Transactions</div>
            <div class="metric-value">{total_transactions:,}</div>
        </div>''', unsafe_allow_html=True)

with metric_col2:
    fraud_count = data[data.get('isfraud', pd.Series([0]*len(data))).astype(int) == 1].shape[0] if 'isfraud' in data.columns else 0
    fraud_percentage = (fraud_count / total_transactions * 100) if total_transactions > 0 else 0
    st.markdown(f'''<div class="metric-card">
            <div class="metric-label">Fraudulent Cases</div>
            <div class="metric-value">{fraud_count:,}</div>
            <div style="color:#e74c3c;font-size:.9rem;">({{fraud_percentage:.1f}}%)</div>
        </div>'''.format(fraud_percentage=fraud_percentage), unsafe_allow_html=True)

with metric_col3:
    total_amount = data.get('amountofmoney', pd.Series([0]*len(data))).sum()
    st.markdown(f'''<div class="metric-card">
            <div class="metric-label">Total Amount</div>
            <div class="metric-value">${{total_amount:,.0f}}</div>
        </div>'''.format(total_amount=total_amount), unsafe_allow_html=True)

with metric_col4:
    avg_transaction = data.get('amountofmoney', pd.Series([0]*len(data))).mean()
    st.markdown(f'''<div class="metric-card">
            <div class="metric-label">Avg Transaction</div>
            <div class="metric-value">${{avg_transaction:,.0f}}</div>
        </div>'''.format(avg_transaction=avg_transaction), unsafe_allow_html=True)

# ---------------------------- SIDEBAR FILTERS ----------------------------
st.sidebar.markdown("## 🔧 Filter Options")
st.sidebar.markdown("---")

def safe_unique(colname):
    return sorted(data[colname].dropna().unique()) if colname in data.columns else []

def pick_all(selected, universe):
    return selected if selected else universe

months = safe_unique("month")
if months:
    st.sidebar.markdown("### 📅 Time Period")
    month_sel = preprocess.multiselect("Select Month", months, default=months)
else:
    month_sel = []

types_actions = safe_unique("typeofaction")
st.sidebar.markdown("### 💼 Transaction Type")
action_sel = preprocess.multiselect("Select Type of Action", types_actions, default=types_actions)

fraud_vals = safe_unique("isfraud")
st.sidebar.markdown("### 🚨 Fraud Status")
fraud_sel = preprocess.multiselect("Select Fraud Status", fraud_vals, default=fraud_vals)

crime_vals = safe_unique("typeofcrime")
st.sidebar.markdown("### 🔴 Crime Classification")
crime_sel = preprocess.multiselect("Select Type of Crime", crime_vals, default=crime_vals)

month_sel = pick_all(month_sel, months)
action_sel = pick_all(action_sel, types_actions)
fraud_sel = pick_all(fraud_sel, fraud_vals)
crime_sel = pick_all(crime_sel, crime_vals)

mask = pd.Series(True, index=data.index)
if months: mask &= data["month"].isin(month_sel)
if types_actions: mask &= data["typeofaction"].isin(action_sel)
if fraud_vals: mask &= data["isfraud"].isin(fraud_sel)
if crime_vals: mask &= data["typeofcrime"].isin(crime_sel)
filtered_df = data[mask]

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Filter Summary")
st.sidebar.info(f"""
**CSV:** {csv_found}  
**Filtered Records:** {len(filtered_df):,}  
**Original Records:** {len(data):,}  
**Percentage:** {(len(filtered_df)/len(data)*100 if len(data) else 0):.1f}%
""")

# ---------------------------- VISUALIZATIONS ----------------------------
st.markdown("---")
st.markdown("## 📊 Analytics Dashboard")

if not filtered_df.empty:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True); plot_daily_transactions(filtered_df); st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-container">', unsafe_allow_html=True); plot_fraud_analysis(filtered_df); st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-container">', unsafe_allow_html=True); plot_distribution_of_transaction_amounts(filtered_df); st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-container">', unsafe_allow_html=True); plot_fraud_type_analysis(filtered_df); st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-container">', unsafe_allow_html=True); plot_heatmap(filtered_df); st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-container">', unsafe_allow_html=True); plot_crime_level_trends(filtered_df); st.markdown('</div>', unsafe_allow_html=True)
else:
    st.warning("⚠️ No data available to display. Please adjust your filters.")

# ---------------------------- FOOTER ----------------------------
st.markdown("---")
footer = """<div class="footer">
    <p style="font-size: 1.2rem; margin-bottom: 0.5rem;">💼 Developed by <b>Team Data Disruptors_007</b></p>
    <p style="margin: 0.5rem 0;">
        <a href="https://www.linkedin.com/in/rahulx2001" target="_blank">👨‍💻 Rahul Kumar Singh</a>
    </p>
    <p style="font-size: 0.9rem; margin-top: 1rem; opacity: 0.8;">
        © 2024 Black Money Detection System | All Rights Reserved
    </p>
</div>
"""
st.markdown(footer, unsafe_allow_html=True)
