
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import MaxNLocator
import warnings
# Suppress warnings
warnings.filterwarnings("ignore")

# ---------------------------------------------- Chart 1: The total amount of money transacted over time----------------------------------------------------

def plot_daily_transactions(filtered_df):
    st.write("") # For giving a line space
    st.write("### Daily Transactions")
    daily_transactions = filtered_df.groupby('date')['amountofmoney'].sum().reset_index()
    plt.figure(figsize=(12, 5))
    sns.lineplot(data=daily_transactions, x='date', y='amountofmoney', marker='8', linewidth=1.5)
    plt.title('Daily Transactions', fontsize=15, fontweight='bold')
    plt.xlabel('Date', fontsize=12, fontweight='bold')
    plt.ylabel('Total Amount of Money', fontsize=12, fontweight='bold')
    locator = MaxNLocator(nbins=20)
    plt.gca().xaxis.set_major_locator(locator)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(plt)

# ---------------------------------------------- Chart 2: Count of fraudulent vs non-fraudulent transactions----------------------------------------------------

def plot_fraud_analysis(filtered_df):
    fraud_counts = filtered_df['isfraud'].value_counts().reset_index()
    fraud_counts.columns = ['Fraud Status', 'Count']
    
    st.write("") # For giving a line space
    
    st.write("### Fraud Analysis")
    st.write("This section provides insights into the count and proportion of fraudulent versus non-fraudulent transactions based on the selected filters.")
    
    col1, col2 = st.columns(2)

    with col1:
        plt.figure(figsize=(6, 4))
        sns.barplot(data=fraud_counts, x='Fraud Status', y='Count', palette='pastel', edgecolor='black')
        plt.title('Count of Fraudulent vs Non-Fraudulent Transactions', fontweight='bold')
        plt.xlabel('Fraud Status (0 = Non-Fraud, 1 = Fraud)', fontweight='bold')
        plt.ylabel('Count of Transactions', fontweight='bold')
        plt.grid(axis='y')
        plt.tight_layout()
        st.pyplot(plt)

    with col2:
        if not fraud_counts.empty:
            labels = ['Fraudulent (1)', 'Non-Fraudulent (0)']
            sizes = [fraud_counts.loc[fraud_counts['Fraud Status'] == 1, 'Count'].values[0] if 1 in fraud_counts['Fraud Status'].values else 0,
                     fraud_counts.loc[fraud_counts['Fraud Status'] == 0, 'Count'].values[0] if 0 in fraud_counts['Fraud Status'].values else 0]
            colors = ['lightblue', 'salmon']
            plt.figure(figsize=(6, 4.95))
            plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140, explode=(0.1, 0))
            plt.title('Proportion of Fraudulent vs Non-Fraudulent Transactions', fontweight='bold', fontsize=16)
            plt.axis('equal')
            plt.tight_layout()
            st.pyplot(plt)
        else:
            st.warning("No data available to display in the pie chart. Please adjust your filters.")

# ------------------------------------------------------- Chart 3: Distribution of Transaction Amounts ---------------------------------------------------------

def plot_distribution_of_transaction_amounts(filtered_df):

    st.write("") # For giving a line space
    
    st.write("### Distribution of Transaction Amounts")
    st.write("This histogram shows how transaction amounts are distributed across different transactions. Each bar represents a range of transaction amounts, and the height of the bar indicates how many transactions fall within that range.")
    
    plt.figure(figsize=(12, 5))
    sns.histplot(filtered_df['amountofmoney'], bins=30, kde=True, color='skyblue', edgecolor='gray')
    plt.title('Distribution of Transaction Amounts', fontsize=16, fontweight='bold')
    plt.xlabel('Amount of Money', fontsize=12, fontweight='bold')
    plt.ylabel('Frequency', fontsize=12, fontweight='bold')

    mean_value = filtered_df['amountofmoney'].mean()
    plt.axvline(mean_value, color='#cc0000', linestyle='dashed', linewidth=2)
    
    max_y = plt.ylim()[1]
    plt.text(mean_value + 10000, max_y * 0.1, f'Mean: {mean_value:.2f}', color='#cc0000', fontsize=12)
    
    plt.grid(axis='y', linestyle='--', alpha=0.3)
    plt.tight_layout()
    st.pyplot(plt)

# ------------------------------------------------------------- Chart 4: Fraud Type Analysis ------------------------------------------------------------------

def plot_fraud_type_analysis(filtered_df):
    st.write("") # For giving a line space
    
    st.write("### Types of Fraud Analysis")
    st.write("This bar chart displays the different types of fraud that have been detected in transactions.")
    
    fraud_type_counts = filtered_df['typeoffraud'].value_counts().reset_index()
    fraud_type_counts.columns = ['Type of Fraud', 'Count']

    plt.figure(figsize=(10, 4))
    sns.barplot(data=fraud_type_counts, x='Type of Fraud', y='Count', palette='rocket')
    plt.title('Types of Fraud Occurring in Transactions', fontsize=13, fontweight='bold')
    plt.xlabel('Type of Fraud', fontsize=11, fontweight='bold')
    plt.ylabel('Count', fontsize=11, fontweight='bold')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--')
    plt.tight_layout()
    st.pyplot(plt)

# ------------------------------------------------------ Chart 5: Heatmap of Crime Levels Over Time ------------------------------------------------------------

def plot_heatmap(filtered_df):
    st.write("") # For giving a line space
    
    st.write("### Heatmap of Total Amount by Crime Level Over Time")
    st.write("This heatmap visualizes the total transaction amounts associated with different levels of crime across various months. Each row represents a specific level of crime, while each column corresponds to a month. The intensity of the colors indicates the total amount transacted, with darker shades representing higher amounts. This visualization helps identify trends and patterns in criminal activity over time, allowing for better analysis and understanding of financial behaviors related to different types of crimes.")
    
    heatmap_data = filtered_df.pivot_table(values='amountofmoney', index='levelofcrime',
                                            columns=filtered_df['month'], aggfunc='sum')

    plt.figure(figsize=(12, 5))
    sns.heatmap(heatmap_data, cmap='magma', annot=True, fmt='.0f',
                linewidths=.5, cbar_kws={'label': 'Total Amount'})
    
    plt.title('Heatmap of Total Amount by Crime Level Over Time',
              fontsize=16, fontweight='bold')
    
    plt.xlabel('Month-Year', fontsize=12, fontweight='bold')
    plt.ylabel('Level of Crime', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    st.pyplot(plt)

# --------------------------------------------------------- Chart 6: Crime Level Trends ---------------------------------------------------------------------
def plot_crime_level_trends(filtered_df):
    st.write("") # For giving a line space
    
    st.write("### Average Transaction Amount by Crime Level Over Time")
    st.write("This line chart illustrates the average transaction amounts associated with different levels of crime over various months. Each line represents a specific level of crime, allowing us to observe how the average transaction amount changes over time. This visualization helps identify trends and patterns in financial activities related to different types of crimes, providing valuable insights into potential shifts in criminal behavior.")
    
    monthly_crime_trends = filtered_df.groupby(['month', 'levelofcrime'])['amountofmoney'].mean().reset_index()
    
    monthly_crime_trends['month'] = monthly_crime_trends['month'].apply(
        lambda x: pd.to_datetime(f'2019-{x}-01').strftime('%B'))
    
    
    plt.figure(figsize=(11, 5))    
    sns.lineplot(data=monthly_crime_trends,
                 x='month',
                 y='amountofmoney',
                 hue='levelofcrime',
                 marker='o')

    plt.title('Average Transaction Amount by Crime Level Over Time',
              fontsize=18,
              fontweight='bold')

    plt.xlabel('Month', fontsize=14)
    plt.ylabel('Average Amount of Money', fontsize=14)
    
    plt.xticks(rotation=45)
    
    plt.grid()
    
    plt.legend(title='Level of Crime', fontsize=12)
    
    plt.tight_layout()
    
    st.pyplot(plt)
