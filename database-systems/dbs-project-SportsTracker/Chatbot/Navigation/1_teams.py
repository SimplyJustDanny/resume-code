import requests
import streamlit as st 
import pandas as pd
import altair as alt

st.header("Teams Page")
st.title("Teams Analytics")

# Side-by-side buttons using columns
# del col3 and st.columns to 2
col1, col2 = st.columns(2)

show_top_teams = False
show_sports_dist = False

base_url = "https://group-abcd-6cd3d84eb4d5.herokuapp.com"


with col1:
    if st.button("Top Teams"):
        # st.session_state.logged_in = False
        show_top_teams = True

with col2:
    if st.button("Sports Distribution"):
        # st.session_state.logged_in = True
        show_sports_dist = True

# Handle full-width content below buttons
if show_top_teams:
    st.subheader("Showing Top Teams...")
    url = base_url + "/teams/top-teams"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    df = pd.DataFrame(data)


    # Convert to numeric for chart (just in case)
    df["championships_won"] = pd.to_numeric(df["championships_won"], errors="coerce")

    # Chart: Top Teams
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X("championships_won:Q", title="Championships Won"),
        y=alt.Y("name:N", sort='-x', title="Team"),
        color=alt.Color("sport:N", title="Sport"),
        tooltip=["name", "sport", "championships_won"]
    ).properties(
        title="Top 3 Teams by Championship Wins",
        width=600
    )

    st.altair_chart(chart, use_container_width=True)

    st.table(df)

if show_sports_dist:
    st.subheader("Showing Sports Distribution...")
    url = base_url + "/teams/sports-distribution"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    df = pd.DataFrame(data)


    # Convert to numeric for chart
    df["team_count"] = pd.to_numeric(df["team_count"], errors="coerce")

    # Chart: Sports Distribution
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X("sport:N", sort='-y', title="Sport"),
        y=alt.Y("team_count:Q", title="Number of Teams"),
        tooltip=["sport", "team_count"]
    ).properties(
        title="Number of Teams per Sport",
        width=600
    )

    st.altair_chart(chart, use_container_width=True)

    st.table(df)
