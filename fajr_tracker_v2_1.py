
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os

st.set_page_config(page_title="🌙 Fajr Tracker", layout="centered")

st.markdown(
    "<h1 style='text-align:center; color:#2E4053;'>🌅 Fajr Tracker v2.1</h1>",
    unsafe_allow_html=True
)

DATA_FILE = "fajr_data.csv"
members = ["Shaheer", "MSN", "Ali"]
fajr_types = {
    "Fajr with Jamaat": 5,
    "Fajr prayed alone": 2,
    "Fajr Qaza": -1
}

if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["Date", "Member", "Fajr Type", "Points"])
    df.to_csv(DATA_FILE, index=False)

df = pd.read_csv(DATA_FILE)
today = datetime.now().date()

# Remove records older than 30 days
if not df.empty:
    df['Date'] = pd.to_datetime(df['Date']).dt.date
    df = df[df['Date'] > today - timedelta(days=30)]
    df.to_csv(DATA_FILE, index=False)

st.sidebar.header("Enter your Fajr record")
selected_member = st.sidebar.selectbox("Select your name", members)
selected_fajr = st.sidebar.selectbox("How did you pray Fajr today?", list(fajr_types.keys()))

if st.sidebar.button("Submit Entry"):
    if ((df["Member"] == selected_member) & (df["Date"] == today)).any():
        st.sidebar.warning("⚠️ You already entered today's Fajr record!")
    else:
        new_entry = pd.DataFrame({
            "Date": [today],
            "Member": [selected_member],
            "Fajr Type": [selected_fajr],
            "Points": [fajr_types[selected_fajr]]
        })
        df = pd.concat([df, new_entry], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.sidebar.success("✅ Entry saved successfully!")

if st.sidebar.button("Reset Today's Entry"):
    before = len(df)
    df = df[~((df["Member"] == selected_member) & (df["Date"] == today))]
    if len(df) < before:
        df.to_csv(DATA_FILE, index=False)
        st.sidebar.success("✅ Your today's entry has been reset.")
    else:
        st.sidebar.info("ℹ️ No entry found for today.")

# Manual refresh button
if st.button("🔄 Refresh Progress"):
    st.experimental_rerun()

st.markdown("---")
st.subheader("📊 Family Progress (Last 30 Days)")

if df.empty:
    st.info("No data yet. Once members start logging, progress will appear here.")
else:
    total_points = df.groupby("Member")["Points"].sum().reindex(members, fill_value=0)
    st.bar_chart(total_points)

    st.markdown("### 🕰️ Daily Records")
    st.dataframe(df.sort_values(by="Date", ascending=False).reset_index(drop=True))
