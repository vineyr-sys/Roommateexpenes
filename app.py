import streamlit as st
import pandas as pd
from datetime import datetime
import os

FILE = "expenses.xlsx"

st.title("Roommate Expense Tracker")

# Input fields
item = st.text_input("Item")
amount = st.number_input("Amount", min_value=0.0)

# Only Viney and Anmol
paid_by = st.selectbox("Paid By", ["Viney", "Anmol"])

if st.button("Add Expense"):
    today = datetime.today().strftime("%Y-%m-%d")
    new_row = {"Date": today, "Item": item, "Amount": amount, "Paid By": paid_by}

    if os.path.exists(FILE):
        df = pd.read_excel(FILE)
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    else:
        df = pd.DataFrame([new_row])

    df.to_excel(FILE, index=False)
    st.success("Expense added!")

# Show table
if os.path.exists(FILE):
    st.subheader("All Expenses")
    df = pd.read_excel(FILE)
    st.dataframe(df)

    # Summary totals
    st.subheader("Summary")
    summary = df.groupby("Paid By")["Amount"].sum()
    st.write(summary)
