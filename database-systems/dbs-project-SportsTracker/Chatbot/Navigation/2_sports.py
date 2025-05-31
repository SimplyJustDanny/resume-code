import requests
import streamlit as st 
import pandas as pd
import altair as alt

st.header("Sports Page")

base_url = "https://group-abcd-6cd3d84eb4d5.herokuapp.com"

st.subheader("Showing Sports Popularity (by Number of Athletes)...")

# Dropdown for number of top sports
limit = st.selectbox("Select number of top sports to display:", [1, 3, 5], index=1)

# Request from the backend  
url = base_url + "/sports/popularity"
response = requests.get(url)
response.raise_for_status()
data = response.json()

# Convert to DataFrame and enforce numeric type
df = pd.DataFrame(data)
df["athlete_count"] = pd.to_numeric(df["athlete_count"], errors="coerce")
df = df.head(limit)

# Create bar chart
chart = alt.Chart(df).mark_bar().encode(
    x=alt.X("athlete_count:Q", title="Number of Athletes"),
    y=alt.Y("sport:N", sort='-x', title="Sport"),
    tooltip=["sport", "athlete_count"]
).properties(
    title=f"Top {limit} Sports by Number of Registered Athletes",
    width=600
)

st.altair_chart(chart, use_container_width=True)

# Display table
st.table(df)