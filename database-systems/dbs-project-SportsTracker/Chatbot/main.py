import streamlit as st
# from streamlit_player import st_player

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = "Obi Wan"


Teams = st.Page(
    "Navigation/1_teams.py", title="Teams", icon=":material/group:", default=False)

Sports = st.Page("Navigation/2_sports.py", title="Sports", icon=":material/sports_football:", default=False )

Championships = st.Page("Navigation/3_championships.py", title="Championships", icon=":material/trophy:", default=False)

Exercises = st.Page("Navigation/4_exercises.py", title="Exercises", icon=":material/fitness_center:", default=False)

login_page = st.Page("Sign_in/5_sign.py", title="Log in", icon=":material/login:", default=False)

Chatbot = st.Page("chatbot.py", title="Chatbot", icon=":material/robot_2:", default=True)

if st.session_state.logged_in:
    pg = st.navigation(
        {
            "Navigation": [Chatbot, Teams, Sports, Championships, Exercises]
        }
    )
else:
    # cuando login oficialmnete se valla colocar se cambia lo que est en el array a login_page
    pg = st.navigation([login_page])

# st.audio("audio/audio-club-amapiano-319840.wav", start_time= 0, loop= True, autoplay=True)
pg.run()