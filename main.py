"""
🔍 Hidden Transaction Detection Dashboard
A Streamlit-based fraud detection and analysis system
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings("ignore")

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================
st.set_page_config(
    page_title="Hidden Transaction Dashboard",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# CUSTOM CSS STYLING
# =============================================================================
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem 3rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.4);
        text-align: center;
    }
    
    .main-header h1 {
        color: white;
        font-size: 2.8rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .main-header p {
        color: rgba(255,255,255,0.9);
        font-size: 1.1rem;
        margin-top: 0.5rem;
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(145deg, #1a1a2e, #16213e);
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(102, 126, 234, 0.3);
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .metric-label {
        color: rgba(255,255,255,0.7);
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 0.5rem;
    }
    
    .metric-delta {
        font-size: 0.85rem;
        margin-top: 0.3rem;
    }
    
    .delta-positive { color: #00d4aa; }
    .delta-negative { color: #ff6b6b; }
    
    /* Section headers */
    .section-header {
        color: white;
        font-size: 1.5rem;
        font-weight: 600;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid rgba(102, 126, 234, 0.5);
    }
    
    /* Chart containers */
    .chart-container {
        background: linear-gradient(145deg, #1a1a2e, #16213e);
        border: 1px solid rgba(102, 126, 234, 0.2);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: white;
    }
    
    /* Footer */
    .footer {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 16px;
        text-align: center;
        margin-top: 3rem;
        color: white;
    }
    
    .footer a {
        color: #ffd700;
        text-decoration: none;
        font-weight: 600;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Data table styling */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# DATA LOADING
# =============================================================================
@st.cache_data
def load_data():
    """Load and preprocess the transaction data"""
    try:
        # Try loading the processed dataset first
        df = pd.read_csv("data/transactions.csv")
    except:
        try:
            df = pd.read_csv("../hiddentranscation/newdataset (1).csv")
        except:
            df = pd.read_csv("../hiddentranscation/dataset1 (1).csv")
            # Add derived columns if missing
            df['date'] = pd.to_datetime(df['date'])
            df['month'] = df['date'].dt.month
    
    # Ensure date column is properly formatted
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
        if 'month' not in df.columns:
            df['month'] = df['date'].dt.month
        if 'day' not in df.columns:
            df['day'] = df['date'].dt.day
        if 'hour' not in df.columns and df['date'].dtype == 'datetime64[ns]':
            try:
                df['hour'] = df['date'].dt.hour
            except:
                df['hour'] = 12  # Default hour
    
    return df

# =============================================================================
# FRAUD TYPE & CRIME LEVEL MAPPINGS
# =============================================================================
FRAUD_TYPE_LABELS = {
    'type1': '💰 Money Laundering (Cash Injection)',
    'type2': '💸 High-Value Transfer Fraud',
    'type3': '🔄 Structuring/Smurfing',
    'none': '✅ Legitimate'
}

CRIME_LEVEL_LABELS = {
    'head': '👤 Mastermind',
    'colleague': '🤝 Accomplice'
}

# Short labels for charts
FRAUD_TYPE_SHORT = {
    'type1': 'Money Laundering',
    'type2': 'High-Value Fraud',
    'type3': 'Structuring',
    'none': 'Legitimate'
}

CRIME_LEVEL_SHORT = {
    'head': 'Mastermind',
    'colleague': 'Accomplice'
}

# Load data
try:
    data = load_data()
    data_loaded = True
except Exception as e:
    st.error(f"Error loading data: {e}")
    data_loaded = False
    data = pd.DataFrame()

# =============================================================================
# HEADER SECTION
# =============================================================================
st.markdown("""
<div class="main-header">
    <h1>🔍 Hidden Transaction Dashboard</h1>
    <p>Advanced Financial Crime Detection & Analysis System</p>
</div>
""", unsafe_allow_html=True)

if not data_loaded:
    st.warning("⚠️ Please ensure the data file exists in the correct location.")
    st.stop()

# =============================================================================
# FRAUD TYPE LEGEND (Collapsible)
# =============================================================================
with st.expander("ℹ️ Understanding Fraud Types & Crime Levels", expanded=False):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🚨 Fraud Type Classification
        
        | Code | Type | Description |
        |------|------|-------------|
        | **type1** | 💰 Money Laundering | Cash injection by crime ring leaders via cash-in transactions |
        | **type2** | 💸 High-Value Fraud | Large unauthorized transfers (~₹66L avg), mostly by accomplices |
        | **type3** | 🔄 Structuring | Multiple smaller transfers to avoid detection (smurfing) |
        | **none** | ✅ Legitimate | Normal transactions or unclassified |
        """)
    
    with col2:
        st.markdown("""
        ### 👥 Crime Level Hierarchy
        
        | Level | Role | Description |
        |-------|------|-------------|
        | **head** | 👤 Mastermind | Leaders who orchestrate the fraud schemes |
        | **colleague** | 🤝 Accomplice | Workers/mules who execute transactions |
        
        ---
        
        💡 **Key Insight**: Type1 frauds are 100% committed by Masterminds, while Type3 are 100% by Accomplices.
        """)

# =============================================================================
# SIDEBAR FILTERS
# =============================================================================
st.sidebar.markdown("## 🎛️ Dashboard Controls")
st.sidebar.markdown("---")

# Date range filter
if 'month' in data.columns:
    st.sidebar.markdown("### 📅 Time Period")
    months = sorted(data['month'].unique())
    month_names = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
                   7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
    month_options = [month_names.get(m, str(m)) for m in months]
    selected_months = st.sidebar.multiselect(
        "Select Months",
        options=months,
        default=months,
        format_func=lambda x: month_names.get(x, str(x))
    )
else:
    selected_months = []

# Transaction type filter
st.sidebar.markdown("### 💳 Transaction Type")
action_types = data['typeofaction'].unique().tolist()
selected_actions = st.sidebar.multiselect(
    "Select Action Types",
    options=action_types,
    default=action_types
)

# Fraud status filter
st.sidebar.markdown("### 🚨 Fraud Status")
fraud_options = {0: "Non-Fraud", 1: "Fraud"}
selected_fraud = st.sidebar.multiselect(
    "Select Status",
    options=[0, 1],
    default=[0, 1],
    format_func=lambda x: fraud_options[x]
)

# Crime type filter (if available)
if 'typeofcrime' in data.columns:
    st.sidebar.markdown("### 🔴 Crime Type")
    crime_types = data['typeofcrime'].unique().tolist()
    selected_crimes = st.sidebar.multiselect(
        "Select Crime Types",
        options=crime_types,
        default=crime_types,
        format_func=lambda x: FRAUD_TYPE_SHORT.get(x, x)
    )
else:
    selected_crimes = data['typeoffraud'].unique().tolist() if 'typeoffraud' in data.columns else []

# Fraud type filter
if 'typeoffraud' in data.columns:
    st.sidebar.markdown("### 🎭 Fraud Type")
    fraud_types_list = data['typeoffraud'].unique().tolist()
    selected_fraud_types = st.sidebar.multiselect(
        "Select Fraud Types",
        options=fraud_types_list,
        default=fraud_types_list,
        format_func=lambda x: FRAUD_TYPE_SHORT.get(x, x)
    )
else:
    selected_fraud_types = []

# Apply filters
filtered_df = data.copy()

if selected_months and 'month' in data.columns:
    filtered_df = filtered_df[filtered_df['month'].isin(selected_months)]
if selected_actions:
    filtered_df = filtered_df[filtered_df['typeofaction'].isin(selected_actions)]
if selected_fraud:
    filtered_df = filtered_df[filtered_df['isfraud'].isin(selected_fraud)]
if selected_crimes and 'typeofcrime' in data.columns:
    filtered_df = filtered_df[filtered_df['typeofcrime'].isin(selected_crimes)]
if selected_fraud_types and 'typeoffraud' in data.columns:
    filtered_df = filtered_df[filtered_df['typeoffraud'].isin(selected_fraud_types)]

# Sidebar summary
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Filter Summary")
filter_pct = (len(filtered_df) / len(data) * 100) if len(data) > 0 else 0
st.sidebar.info(f"""
**Filtered:** {len(filtered_df):,} records  
**Total:** {len(data):,} records  
**Coverage:** {filter_pct:.1f}%
""")

# =============================================================================
# KEY METRICS
# =============================================================================
st.markdown('<div class="section-header">📈 Key Performance Indicators</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_transactions = len(filtered_df)
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{total_transactions:,}</div>
        <div class="metric-label">Total Transactions</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    fraud_count = filtered_df[filtered_df['isfraud'] == 1].shape[0]
    fraud_pct = (fraud_count / total_transactions * 100) if total_transactions > 0 else 0
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{fraud_count:,}</div>
        <div class="metric-label">Fraudulent Cases</div>
        <div class="metric-delta delta-negative">({fraud_pct:.1f}% of total)</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    total_amount = filtered_df['amountofmoney'].sum()
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">₹{total_amount/1e6:.1f}M</div>
        <div class="metric-label">Total Amount</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    fraud_amount = filtered_df[filtered_df['isfraud'] == 1]['amountofmoney'].sum()
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">₹{fraud_amount/1e6:.1f}M</div>
        <div class="metric-label">Fraud Amount</div>
        <div class="metric-delta delta-negative">At Risk</div>
    </div>
    """, unsafe_allow_html=True)

# =============================================================================
# CHARTS ROW 1: Transaction Trends & Fraud Analysis
# =============================================================================
st.markdown('<div class="section-header">📊 Transaction Analytics</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    
    # Daily transaction trend
    if 'date' in filtered_df.columns:
        daily_data = filtered_df.groupby(filtered_df['date'].dt.date)['amountofmoney'].sum().reset_index()
        daily_data.columns = ['Date', 'Amount']
        
        fig = px.area(
            daily_data, x='Date', y='Amount',
            title='📈 Daily Transaction Volume',
            color_discrete_sequence=['#667eea']
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            title_font_size=16,
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)')
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    
    # Fraud vs Non-Fraud pie chart
    fraud_counts = filtered_df['isfraud'].value_counts().reset_index()
    fraud_counts.columns = ['Status', 'Count']
    fraud_counts['Status'] = fraud_counts['Status'].map({0: 'Legitimate', 1: 'Fraudulent'})
    
    fig = px.pie(
        fraud_counts, values='Count', names='Status',
        title='🔴 Fraud vs Legitimate Transactions',
        color_discrete_sequence=['#00d4aa', '#ff6b6b'],
        hole=0.4
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        title_font_size=16
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# =============================================================================
# CHARTS ROW 2: Transaction Types & Amount Distribution
# =============================================================================
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    
    # Transaction types bar chart
    action_counts = filtered_df['typeofaction'].value_counts().reset_index()
    action_counts.columns = ['Type', 'Count']
    
    fig = px.bar(
        action_counts, x='Type', y='Count',
        title='💳 Transaction Types Distribution',
        color='Count',
        color_continuous_scale='Viridis'
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        title_font_size=16,
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)')
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    
    # Amount distribution histogram
    fig = px.histogram(
        filtered_df, x='amountofmoney',
        title='💰 Transaction Amount Distribution',
        nbins=30,
        color_discrete_sequence=['#764ba2']
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        title_font_size=16,
        xaxis=dict(showgrid=False, title='Amount (₹)'),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', title='Frequency')
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# =============================================================================
# CHARTS ROW 3: Fraud Type Analysis & Crime Level Heatmap
# =============================================================================
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    
    # Fraud types analysis
    if 'typeoffraud' in filtered_df.columns:
        fraud_types = filtered_df['typeoffraud'].value_counts().reset_index()
        fraud_types.columns = ['Fraud Type', 'Count']
        # Map to readable labels
        fraud_types['Fraud Type Label'] = fraud_types['Fraud Type'].map(FRAUD_TYPE_SHORT)
        
        fig = px.bar(
            fraud_types, x='Fraud Type Label', y='Count',
            title='🚨 Types of Fraud Detected',
            color='Fraud Type Label',
            color_discrete_map={
                'Money Laundering': '#ff6b6b',
                'High-Value Fraud': '#feca57',
                'Structuring': '#ff9ff3',
                'Legitimate': '#00d4aa'
            }
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            title_font_size=16,
            showlegend=False,
            xaxis=dict(showgrid=False, title='Fraud Type'),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)')
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    
    # Crime level by month heatmap
    if 'levelofcrime' in filtered_df.columns and 'month' in filtered_df.columns:
        # Create copy and map labels
        heatmap_df = filtered_df.copy()
        heatmap_df['Crime Role'] = heatmap_df['levelofcrime'].map(CRIME_LEVEL_SHORT)
        
        heatmap_data = heatmap_df.pivot_table(
            values='amountofmoney',
            index='Crime Role',
            columns='month',
            aggfunc='sum'
        ).fillna(0)
        
        fig = px.imshow(
            heatmap_data,
            title='🔥 Crime Role vs Month Heatmap',
            color_continuous_scale='Magma',
            labels=dict(x='Month', y='Crime Role', color='Amount (₹)')
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            title_font_size=16
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Heatmap requires 'levelofcrime' and 'month' columns")
    
    st.markdown('</div>', unsafe_allow_html=True)

# =============================================================================
# DATA TABLE
# =============================================================================
st.markdown('<div class="section-header">📋 Transaction Details</div>', unsafe_allow_html=True)

with st.expander("🔽 View Raw Data", expanded=False):
    st.dataframe(
        filtered_df.head(100).style.background_gradient(subset=['amountofmoney'], cmap='Blues'),
        use_container_width=True
    )
    
    # Download button
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv,
        file_name="filtered_transactions.csv",
        mime="text/csv"
    )

# =============================================================================
# FOOTER
# =============================================================================
st.markdown("""
<div class="footer">
    <p style="font-size: 1.2rem; margin-bottom: 0.5rem;">
        💼 Developed by <b>Rahul Kumar Singh</b>
    </p>
    <p style="margin: 0.5rem 0;">
        <a href="https://www.linkedin.com/in/rahulx2001" target="_blank">
            🔗 Connect on LinkedIn
        </a>
    </p>
    <p style="font-size: 0.9rem; margin-top: 1rem; opacity: 0.8;">
        © 2024 Hidden Transaction Detection System | All Rights Reserved
    </p>
</div>
""", unsafe_allow_html=True)
