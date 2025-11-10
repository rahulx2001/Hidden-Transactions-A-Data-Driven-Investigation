import pandas as pd
import numpy as np
import streamlit as st


# Multiselect function
def multiselect(title, options_list):
    selected = st.sidebar.multiselect(title, options_list)
    select_all = st.sidebar.checkbox("Select all", value = True, key = title)
    if select_all:
        selected_options = options_list
    else:
        selected_options = selected
    return selected_options

'''
def get_transaction_insights(data):
    """Get insights on highest transactions by cash, by bank and month with most transactions."""
    # Convert 'date' to datetime if not already done
    data['date'] = pd.to_datetime(data['date'], errors='coerce')  # Use 'coerce' to handle invalid dates
    
    # Debug: Check for any NaT values in 'date'
    if data['date'].isnull().any():
        print("Warning: Some dates could not be parsed and have been set to NaT.")
    
    # Filter for cash-in transactions
    cash_in_data = data[data['typeofaction'] == 'cash-in']
    
    # Find highest cash transaction
    if not cash_in_data.empty:
        highest_cash_transaction = cash_in_data.loc[cash_in_data['amountofmoney'].idxmax()]
        highest_cash_amount = highest_cash_transaction['amountofmoney']
        highest_cash_date = highest_cash_transaction['date']
    else:
        highest_cash_amount = None
        highest_cash_date = None

    # Filter for transfer transactions
    transfer_data = data[data['typeofaction'] == 'transfer']
    
    # Find highest transfer transaction
    if not transfer_data.empty:
        highest_transfer_transaction = transfer_data.loc[transfer_data['amountofmoney'].idxmax()]
        highest_transfer_amount = highest_transfer_transaction['amountofmoney']
        highest_transfer_date = highest_transfer_transaction['date']
    else:
        highest_transfer_amount = None
        highest_transfer_date = None

    # Find month with most transactions
    if 'date' in data.columns and not data['date'].isnull().all():
        data['month'] = data['date'].dt.to_period('M')  # Extract year-month
        most_transactions_month = data['month'].value_counts().idxmax() if not data['month'].empty else None  # Month with most transactions
    else:
        most_transactions_month = None

    return {
        'highest_cash_amount': highest_cash_amount,
        'highest_cash_date': highest_cash_date,
        'highest_transfer_amount': highest_transfer_amount,
        'highest_transfer_date': highest_transfer_date,
        'most_transactions_month': most_transactions_month
    }


'''
