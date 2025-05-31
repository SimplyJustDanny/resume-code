import requests
import streamlit as st 
import pandas as pd
import altair as alt

st.header("Exercise Page")
st.title("Exercises Analytics")

base_url = "https://group-abcd-6cd3d84eb4d5.herokuapp.com"

selection = st.radio(
    "What do you wish to see?",
    ["Most Performed Exercises", "Muscle Groups", "Most Complex Exercises"]
)

if selection == "Most Performed Exercises":
    st.subheader("Top Exercises Used in Sports")
    url = base_url + "/exercises/most-performed"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    df = pd.DataFrame(data)

    st.table(df)

    # Convert numeric column
    df["sports_related"] = pd.to_numeric(df["sports_related"], errors="coerce")

    # Bar chart
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X("sports_related:Q", title="Number of Sports"),
        y=alt.Y("name:N", sort='-x', title="Exercise"),
        tooltip=["name", "sports_related"]
    ).properties(
        title="Most Performed Exercises Across Sports",
        width=600
    )

    st.altair_chart(chart, use_container_width=True)

elif selection == "Muscle Groups":
    muscle_text = st.text_input("Enter Muscle Name (e.g., Chest, Biceps)")
    muscle_text = muscle_text.lower()
    if st.button("Show Muscle Group"):
        if muscle_text.strip() == "":
            st.warning("Please enter a muscle name.")
        else:
            st.subheader(f"Exercises Targeting Muscle: {muscle_text}")
            url = base_url + "/exercises/muscle-group"
            params = {"muscle": muscle_text}
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            df = pd.DataFrame(data)
            if df.empty:
                st.info("No exercises found for this muscle.")
            else:
                st.table(df)

elif selection == "Most Complex Exercises":
    st.subheader("Showing Most Complex Exercises...")
    url = base_url + "/exercises/most-complex"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    df = pd.DataFrame(data)

    import altair as alt

    if "muscle_groups" in df.columns:
        df["muscle_count"] = df["muscle_groups"].apply(lambda m: len(m) if isinstance(m, list) else 0)
        df["muscle_groups"] = df["muscle_groups"].apply(lambda m: ", ".join(m) if isinstance(m, list) else "")
        st.dataframe(df)

        st.subheader("Complexity by Muscle Count")
        chart = alt.Chart(df).mark_bar().encode(
            y=alt.Y('name:N', title='Exercise Name', sort='-x'),
            x=alt.X('muscle_count:Q', title='Number of Muscles Involved'),
            tooltip=['name', 'muscle_count']
        ).properties(
            width=700,
            height=500
        )
        st.altair_chart(chart, use_container_width=True)


    else:
        st.error("Expected 'muscle_groups' field not found in response.")
        st.write("Response data:", df)