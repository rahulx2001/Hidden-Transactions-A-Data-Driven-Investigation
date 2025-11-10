import pandas as pd
import numpy as np
import streamlit as st

# ✅ Updated multiselect function with default support
def multiselect(title, options_list, default=None):
    """
    Custom multiselect with select-all option.
    Compatible with Streamlit's default= parameter.
    """

    # If default not provided → show all as default
    if default is None:
        default = options_list

    # Main multiselect widget
    selected = st.sidebar.multiselect(title, options_list, default=default)

    # Select-all checkbox
    select_all = st.sidebar.checkbox("Select all", value=True, key=title)

    # If "Select all" is checked → override selected list
    if select_all:
        return options_list
    else:
        return selected


"""
Extra helper functions (if needed later) can be added below.
"""
