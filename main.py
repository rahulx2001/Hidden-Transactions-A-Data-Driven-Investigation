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
data = pd.read_csv("merged_data.csv")

# Set up your Streamlit page configuration
#Adjusting the tab image and name
st.set_page_config(page_icon='Black Money.png', page_title='Black Money Dashboard', layout='wide')

# --------------------------------------------------------------- LOGO AND OBJECTIVE PART------------------------------------------------------------------

col11,col14 = st.columns([1,5])

with col11:
    st.write("")
    st.write("")
    
    st.image('Black Money.png', width=200, use_container_width=False)    

# Dashboard Details Section
with col14:
    st.title('Black Money Dashboard')
    st.write("The objective of the black money dashboard project is to develop a robust analytical tool that facilitates the monitoring and detection of fraudulent financial activities associated with black money. By utilizing a dataset that includes transaction details such as the type of action, source and destination IDs, transaction amounts, fraud indicators, and crime classifications, the dashboard aims to provide insights into suspicious transactions. This will help identify patterns of cash inflow that may indicate illicit financial behavior. The project seeks to enhance transparency in financial transactions, support regulatory compliance, and assist law enforcement agencies in their efforts to combat financial crimes. Ultimately, the dashboard will serve as a critical resource for understanding and mitigating the risks associated with black money in the economy.")

# ---------------------------------------------------------------- SIDEBAR AND FILTERING -----------------------------------------------------------------------

# Sidebar for filtering options
st.sidebar.title("Filter Options")

# Check if 'month' column exists before accessing it
if 'month' in data.columns:
    selected_month = preprocess.multiselect("Select Month", data["month"].unique())
else:
    st.error("The 'month' column is not available in the data.")

selected_action = preprocess.multiselect("Select Type of Action", data["typeofaction"].unique())
selected_isfraud = preprocess.multiselect("Select Fraud Status", data["isfraud"].unique())
selected_typeofcrime = preprocess.multiselect("Select Type of Crime", data["typeofcrime"].unique())

filtered_df = data[
    (data["month"].isin(selected_month)) & 
    (data["typeofaction"].isin(selected_action)) & 
    (data["isfraud"].isin(selected_isfraud))&
    (data["typeofcrime"].isin(selected_typeofcrime))
]

# ------------------------------------------------------------------- VISUALIZATIONS---------------------------------------------------------------

if not filtered_df.empty:
   # Call the plotting functions from charts.py
   plot_daily_transactions(filtered_df)
   plot_fraud_analysis(filtered_df)
   plot_distribution_of_transaction_amounts(filtered_df)
   plot_fraud_type_analysis(filtered_df)
   plot_heatmap(filtered_df)
   plot_crime_level_trends(filtered_df)
else:
   st.warning("No data available to display. Please adjust your filters.")

# Footer
footer = """
<style>
a:link, a:visited {
    color: red;
    background-color: transparent;
    text-decoration: solid;
}

a:hover, a:active {
    color: blue;
    background-color: transparent;
    text-decoration: solid;
}

.footer {
    position: relative; /* Make footer relative to the content */
    bottom: 0;
    width: 100%;
    background-color: white;
    color: black;
    text-align: center;
    font-size: 18px;
    margin-top: 20px;
    padding: 20px 0; /* Adds padding inside the footer */
    border-top: 1px solid #ddd; /* Optional: Add a subtle top border */
}
</style>
<div class="footer">
    <p> Developed by <b> Team Data Disruptors_007</b> </p>
    <p> 
        <a href="https://www.linkedin.com/in/rahulx2001" target="_blank">Rahul Kumar Singh </a>, 
              
    </p>
</div>
"""
st.markdown(footer, unsafe_allow_html=True)
