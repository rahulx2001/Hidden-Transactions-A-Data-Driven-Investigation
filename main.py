# main.py
import streamlit as st
import pandas as pd
import preprocess

from charts import (
   plot_daily_transactions,
   plot_fraud_analysis,
   plot_distribution_of_transaction_amounts,
   plot_fraud_type_analysis,
   plot_heatmap,
   plot_crime_level_trends
)

# ---------------------------------------------------------DATA LOADING AND PAGE CONFIGURATIONS------------------------------------------------------------

# Load your data
data = pd.read_csv("dataset1.csv")

# Set up your Streamlit page configuration
st.set_page_config(
    page_icon='Blackmoney.png', 
    page_title='Black Money Dashboard', 
    layout='wide',
    initial_sidebar_state='expanded'
)

# Custom CSS for better styling
st.markdown("""
    <style>
    /* Main container styling */
    .main {
        padding: 0rem 1rem;
    }
    
    /* Header styling */
    .dashboard-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .dashboard-title {
        color: white;
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0;
        text-align: center;
    }
    
    .dashboard-subtitle {
        color: #f0f0f0;
        font-size: 1rem;
        text-align: center;
        margin-top: 0.5rem;
    }
    
    /* Logo container */
    .logo-container {
        text-align: center;
        padding: 1rem;
    }
    
    /* Objective section styling */
    .objective-section {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #667eea;
        margin: 2rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .objective-title {
        color: #667eea;
        font-size: 1.3rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    
    .objective-text {
        color: #444;
        line-height: 1.6;
        text-align: justify;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #f8f9fa;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: white;
    }
    
    /* Metric cards */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #667eea;
    }
    
    .metric-label {
        color: #666;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Footer styling */
    .footer {
        position: relative;
        bottom: 0;
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        text-align: center;
        font-size: 16px;
        margin-top: 3rem;
        padding: 2rem 0;
        border-radius: 10px;
        box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
    }
    
    .footer a {
        color: #ffd700;
        text-decoration: none;
        font-weight: bold;
        transition: color 0.3s;
    }
    
    .footer a:hover {
        color: #ffed4e;
        text-decoration: underline;
    }
    
    /* Chart containers */
    .chart-container {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        margin: 1.5rem 0;
    }
    
    /* Warning message styling */
    .stAlert {
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --------------------------------------------------------------- LOGO AND HEADER SECTION ------------------------------------------------------------------

# Header with logo and title
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    st.image('Blackmoney.png', width=150)
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

# Dashboard Objective Section
st.markdown("""
    <div class="objective-section">
        <div class="objective-title">📊 Dashboard Objective</div>
        <div class="objective-text">
            This advanced analytical tool monitors and detects fraudulent financial activities associated with black money. 
            By analyzing transaction details including action types, source/destination IDs, amounts, fraud indicators, and 
            crime classifications, the dashboard provides actionable insights into suspicious transactions. It helps identify 
            patterns of illicit cash flow, enhances financial transparency, supports regulatory compliance, and assists law 
            enforcement agencies in combating financial crimes.
        </div>
    </div>
""", unsafe_allow_html=True)

# Key Metrics Section
st.markdown("### 📈 Key Metrics")
metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

with metric_col1:
    total_transactions = len(data)
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Transactions</div>
            <div class="metric-value">{total_transactions:,}</div>
        </div>
    """, unsafe_allow_html=True)

with metric_col2:
    fraud_count = data[data['isfraud'] == 1].shape[0]
    fraud_percentage = (fraud_count / total_transactions * 100) if total_transactions > 0 else 0
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Fraudulent Cases</div>
            <div class="metric-value">{fraud_count:,}</div>
            <div style="color: #e74c3c; font-size: 0.9rem;">({fraud_percentage:.1f}%)</div>
        </div>
    """, unsafe_allow_html=True)

with metric_col3:
    total_amount = data['amountofmoney'].sum()
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Amount</div>
            <div class="metric-value">${total_amount:,.0f}</div>
        </div>
    """, unsafe_allow_html=True)

with metric_col4:
    avg_transaction = data['amountofmoney'].mean()
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Avg Transaction</div>
            <div class="metric-value">${avg_transaction:,.0f}</div>
        </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------------- SIDEBAR AND FILTERING -----------------------------------------------------------------------

# Sidebar for filtering options
st.sidebar.markdown("## 🔧 Filter Options")
st.sidebar.markdown("---")

# Check if 'month' column exists before accessing it
if 'month' in data.columns:
    st.sidebar.markdown("### 📅 Time Period")
    selected_month = preprocess.multiselect("Select Month", sorted(data["month"].unique()))
else:
    st.error("⚠️ The 'month' column is not available in the data.")
    selected_month = []

st.sidebar.markdown("### 💼 Transaction Type")
selected_action = preprocess.multiselect("Select Type of Action", data["typeofaction"].unique())

st.sidebar.markdown("### 🚨 Fraud Status")
selected_isfraud = preprocess.multiselect("Select Fraud Status", data["isfraud"].unique())

st.sidebar.markdown("### 🔴 Crime Classification")
selected_typeofcrime = preprocess.multiselect("Select Type of Crime", data["typeofcrime"].unique())

# Filter data
filtered_df = data[
    (data["month"].isin(selected_month)) & 
    (data["typeofaction"].isin(selected_action)) & 
    (data["isfraud"].isin(selected_isfraud)) &
    (data["typeofcrime"].isin(selected_typeofcrime))
]

# Display filter summary
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Filter Summary")
st.sidebar.info(f"""
**Filtered Records:** {len(filtered_df):,}  
**Original Records:** {len(data):,}  
**Percentage:** {(len(filtered_df)/len(data)*100):.1f}%
""")

# ------------------------------------------------------------------- VISUALIZATIONS---------------------------------------------------------------

st.markdown("---")
st.markdown("## 📊 Analytics Dashboard")

if not filtered_df.empty:
    # Call the plotting functions from charts.py
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    plot_daily_transactions(filtered_df)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    plot_fraud_analysis(filtered_df)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    plot_distribution_of_transaction_amounts(filtered_df)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    plot_fraud_type_analysis(filtered_df)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    plot_heatmap(filtered_df)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    plot_crime_level_trends(filtered_df)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.warning("⚠️ No data available to display. Please adjust your filters.")

# Footer
st.markdown("---")
footer = """
<div class="footer">
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
