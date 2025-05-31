import requests
import streamlit as st 
import pandas as pd
import altair as alt

st.header("Championships Page")

base_url = "https://group-abcd-6cd3d84eb4d5.herokuapp.com"

st.subheader("Top Teams with Most Championship Wins")

# Dropdown to allow user to choose how many top teams to show
limit = st.selectbox("Select number of top teams to display:", [1, 3, 5], index=1)

# Request data
url = base_url + "/championships/most-wins"
response = requests.get(url)
response.raise_for_status()
data = response.json()

# Convert to DataFrame
df = pd.DataFrame(data)
df["total_wins"] = pd.to_numeric(df["total_wins"], errors="coerce")
df = df.head(limit)

# Bar chart
chart = alt.Chart(df).mark_bar().encode(
    x=alt.X("total_wins:Q", title="Total Championship Wins"),
    y=alt.Y("name:N", sort='-x', title="Team"),
    tooltip=["name", "total_wins"]
).properties(
    title=f"Top {limit} Teams by Championship Wins",
    width=600
)

st.altair_chart(chart, use_container_width=True)

# Display table
st.table(df)
