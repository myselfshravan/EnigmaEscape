import streamlit as st

st.set_page_config(page_title="Enigma Escape", page_icon="🔐")

from api import auth, add_points, get_points, levels_done
from levels import levels
from nemo import EnigmaEscape

st.title("Enigma Escape")
st.subheader("Embark on a linguistic adventure.")

st.session_state["user"] = st.session_state.get("user", None)

if st.session_state["user"] is None:
    with st.form("login"):
        st.info("You can use **enigmaescape** as teamname and password to login")
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


@st.cache_resource
def get_ee():
    return EnigmaEscape(levels)


with get_ee() as bot:
    done_levels = levels_done(st.session_state["user"], [lev.name for lev in bot.levels])
    with st.expander("Choose Level >"):
        bot.set_level(st.radio("Level", options=range(len(levels)),
                               format_func=lambda
                                   x: f"{levels[x].name}: {levels[x].points} points {'✅' if done_levels[x] else '❌'}"))
    st.markdown(f"""
    <h4>Make the bot say the Enigma Phrase <br><span style="color: #ff0000">{bot.level.phrase}</span><br> to escape this level</h4>
    """, unsafe_allow_html=True)
    with st.form("chat"):
        points_holder = st.empty()
        st.session_state["curr_points"] = get_points(st.session_state["user"])
        points_holder.info(f"Points: {st.session_state['curr_points']}")
        que = st.text_area("Enter your instructions to Bot: ", height=100)
        if st.form_submit_button("Send"):
            with st.container():
                with st.spinner("Generating Response..."):
                    resp = bot.chat(que)
                content, _type = resp["content"], resp["type"]
                st.write("AI Bot Response: ")
                if _type == "error":
                    st.error(content)
                elif _type == "info":
                    st.info(content)
                elif _type == "warning":
                    st.warning(content)
                elif _type == "success":
                    st.success(content)
                    st.success(f"hurray! you escaped and gained some points")
                    add_points(st.session_state["user"], bot.level.points, bot.level.name, resp["tokens"], que)
                    st.session_state["curr_points"] = get_points(st.session_state["user"])
                    points_holder.info(f"Points: {st.session_state['curr_points']}")
                else:
                    st.write(content)
