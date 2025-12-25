import streamlit as st
import pandas as pd
from datetime import datetime
import os

FILE = "expenses.xlsx"

st.title("Roommate Expense Tracker")

# Input fields
item = st.text_input("Item")
amount = st.number_input("Amount", min_value=0.0)
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

    # -----------------------------
    # SUMMARY: Who paid how much
    # -----------------------------
    st.subheader("Summary: Total Paid by Each Person")
    totals = df.groupby("Paid By")["Amount"].sum()
    st.write(totals)

    # -----------------------------
    # WHO OWES HOW MUCH
    # -----------------------------
    st.subheader("Who Owes How Much")

    total_spent = df["Amount"].sum()
    split_amount = total_spent / 2  # equal split

    viney_paid = totals.get("Viney", 0)
    anmol_paid = totals.get("Anmol", 0)

    viney_balance = viney_paid - split_amount
    anmol_balance = anmol_paid - split_amount

    if viney_balance > 0:
        st.write(f"Anmol owes Viney: ₹{abs(anmol_balance):.2f}")
    elif anmol_balance > 0:
        st.write(f"Viney owes Anmol: ₹{abs(viney_balance):.2f}")
    else:
        st.write("Both are settled.")

    # -----------------------------
    # MONTHLY TOTALS
    # -----------------------------
    st.subheader("Monthly Totals")

    df["Date"] = pd.to_datetime(df["Date"])
    df["Month"] = df["Date"].dt.to_period("M").astype(str)

    monthly_totals = df.groupby("Month")["Amount"].sum()
    st.write(monthly_totals)
