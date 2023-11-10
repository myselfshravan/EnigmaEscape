import streamlit as st

st.set_page_config(page_title="Enigma Escape", page_icon="🔐")

from api import auth, add_points, get_points
from levels import levels
from nemo import EnigmaEscape

st.title("Enigma Escape")
st.subheader("Embark on a linguistic adventure.")

st.session_state["user"] = st.session_state.get("user", None)

if st.session_state["user"] is None:
    with st.form("login"):
        teamname = st.text_input("Team Name")
        password = st.text_input("Password", type="password")
        if st.form_submit_button("Login"):
            user = auth(teamname, password)
            if user is not None:
                st.session_state["user"] = user
                st.rerun()
            else:
                st.error("Invalid credentials")
        st.stop()

st.write(
    "The game where you guide Bot to say specific phrases with your own cleverly tweaked instructions."
    "Keep it short and smart – change up the words just enough to pass the test and hit the target phrase."
    "Ready, set, twist!"
)

with EnigmaEscape(levels) as bot:
    bot.set_level(st.radio("Level", options=range(len(levels)), format_func=lambda x: f"{levels[x].name}: {levels[x].points} points"))
    st.markdown(f"""
    <h4>Make the bot say the Enigma Phrase <span style="color: #ff0000">{bot.level.phrase}</span> to escape this level</h4>
    """, unsafe_allow_html=True)
    with st.form("chat"):
        st.info(f"Points: {get_points(st.session_state['user'])}")
        que = st.text_area("Enter your instructions here:", height=100)
        if st.form_submit_button("Send"):
            with st.container():
                resp = bot.chat(que)
                content, _type = resp["content"], resp["type"]
                st.write("Bot: ")
                if _type == "error":
                    st.error(content)
                elif _type == "info":
                    st.info(content)
                elif _type == "warning":
                    st.warning(content)
                elif _type == "success":
                    st.success(content)
                    st.success(f"hurray! you have earned {bot.level.points} points")
                    add_points(st.session_state["user"], bot.level.points, bot.level.name, bot.level.max_token)
                else:
                    st.write(content)
