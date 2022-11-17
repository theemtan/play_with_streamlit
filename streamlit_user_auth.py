import pickle
import datetime
from datetime import date, timedelta
from pathlib import Path

import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
import streamlit_authenticator as stauth  # pip install streamlit-authenticator


# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:", layout="wide")


# --- USER AUTHENTICATION ---
names = ["Peter Parker", "Rebecca Miller"]
usernames = ["pparker", "rmiller"]

# load hashed passwords
file_path = "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
    "sales_dashboard", "abcdef", cookie_expiry_days=30)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status == None:
    st.warning("Please enter your username and password")

if authentication_status:
    # ---- READ EXCEL ----
    @st.cache
    def get_data():
        df = pd.read_csv(
            "online_retail_dataset.csv",
            engine="python",
            usecols=["Country","Customer_ID","Invoice_Date","No_of_Rows","Unit_Price","Quantity","Sales_Amount"]
        )
        return df

    df = get_data()

    authenticator.logout("Logout","sidebar")
    st.sidebar.title("Welcome, f{name}")
    st.sidebar.subheader("Please Select The Filters Here:")

    country = st.sidebar.multiselect(
      "Select Country:",
      options=df["Country"].unique(),
      default=df["Country"].unique()
    )

    last_day_prev_month = date.today().replace(day=1) - timedelta(days=1)

    start_day_prev_month = date.today().replace(day=1) - timedelta(days=last_day_prev_month.day)

    start_date = st.sidebar.date_input('Start date', start_day_prev_month)
    end_date = st.sidebar.date_input('End date', last_day_prev_month)
    if start_date < end_date:
        st.success('Start date: `%s`\n\nEnd date:`%s`' % (start_date, end_date))
    else:
        st.error('Error: End date must fall after start date.')

    df_selection = df.query(
        "Country ==@Country"
    )

    # ---- MAINPAGE ----
    st.title(":chart: Dashboard")
    st.markdown("##")

    total_sales = int(df_selection["Sales_Amount"].sum())
    total_transactions = df.selection["No_of_Rows"].sum()
    total_unit_sold = df.selection["Unit_Price"].sum()

    left_column, middle_column, right_column = st.columns(3)
    with left_column:
        st.subheader("Total Sales:")
        st.metric(f"USD $ {total_sales:,}")
    with middle_column:
        st.subheader("Total Transactions:")
        st.metric(f"{total_transactions:}")
    with right_column:
        st.subheader("Total Unit Sold:")
        st.metric(f"{total_unit_sold:}")

    st.markdown("""---""")

