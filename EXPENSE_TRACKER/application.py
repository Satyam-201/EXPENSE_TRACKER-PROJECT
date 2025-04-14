import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import pandas as pd


total_amount=0
if "expenses" not in st.session_state:
    st.session_state.expenses = pd.DataFrame(
        columns=["Date", "Category", "Amount", "Description"]
    )

def add_expense(date, category, amount, description):
    new_expense = pd.DataFrame(
        [[date, category, amount, description]],
        columns=st.session_state.expenses.columns,
    )
    st.session_state.expenses = pd.concat(
        [st.session_state.expenses, new_expense], ignore_index=True
    )


def save_expense():
    st.session_state.expenses.to_csv("expenses.csv", index=False)
    st.success("File Saved Successfully")


def visualise_expense():
    if not st.session_state.expenses.empty:
        fig, ax = plt.subplots()
        sns.barplot(data=st.session_state.expenses, x="Category", y="Amount", ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)
    else:
        st.warning("No Expense To Visualise")


st.title("Expense Tracker App")
with st.sidebar:
    st.header("Add New Expenses ")
    date = st.date_input("Date")
    category = st.selectbox(
        "Category", ["Food", "Transport", "Movie", "Tour", "Others"]
    )
    amount = st.number_input("Amount", format=("%.2f"))
    description = st.text_input("Description")
    if st.button("Add"):
        add_expense(date, category, amount, description)
        st.success("Expense Added Successfully")
    st.header("File Operation")
    if st.button("Save Expense"):
        save_expense()
    file = st.file_uploader("Choose A File To Upload", type=["csv"])
    if file is not None:
        st.session_state.expenses = pd.read_csv(file)
        st.success("File Loaded Successfully")

st.header("Expenses")
st.write(st.session_state.expenses)
total = st.session_state.expenses["Amount"].sum()
st.write(f"💰 Total Expense: ₹{total:.2f}")

st.header("Visualise Expenses")
if st.button("Visualise"):
    visualise_expense()
