import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1.base_query import FieldFilter
import streamlit as st


@st.cache_resource
def get_db():
    try:
        cred = credentials.Certificate("enigmaescape-6506f-firebase-adminsdk-nqhe6-a2b5dacb8d.json")
    except FileNotFoundError:
        cred = credentials.Certificate({
            "type": "service_account",
            "project_id": "enigmaescape-6506f",
            "private_key_id": st.secrets["private_key_id"],
            "private_key": st.secrets["private_key"],
            "client_email": st.secrets["client_email"],
            "client_id": st.secrets["client_id"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": st.secrets["client_x509_cert_url"],
            "universe_domain": "googleapis.com",
        })
    firebase_admin.initialize_app(cred)
    return firestore.client()


db = get_db()
users_col = db.collection(u'users')
points_col = db.collection(u'points')


def auth(teamname, password):
    user = users_col.where(filter=FieldFilter(u'teamname', u'==', teamname)).where(
        filter=FieldFilter(u'password', u'==', password)).get()
    if user and user[0].exists: return user[0]


def add_points(user, points: int, level: int, tokens: int, prompt: str):
    scores = user.reference.get().to_dict().get('scores', {})
    tokens_next = min(tokens, scores.get(str(level), {}).get('tokens', tokens))
    print(prompt)
    user.reference.update({u'scores.' + str(level): {
        u'points': points,
        u'tokens': tokens_next,
        u'best_prompt': prompt if tokens <= tokens_next else scores.get(str(level), {}).get("best_prompt", ""),
        u'done': True,
        # u'response_list': scores.get(str(level), {}).get("response_list", []) + [prompt],
    }})


def get_points(user):
    scores = user.reference.get().to_dict().get('scores', {})
    return sum(
        score.get('points', score.get('tokens', 0)) - score.get('tokens', 0) for score in scores.values()
    )


def levels_done(user, levels):
    scores = user.reference.get().to_dict().get('scores', {})
    return [scores.get(lev, {}).get("done", False) for lev in levels]


if __name__ == '__main__':
    pass
