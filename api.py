import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1.base_query import FieldFilter
import streamlit as st


@st.cache_resource
def get_db():
    cred = credentials.Certificate("enigmaescape-6506f-firebase-adminsdk-nqhe6-a2b5dacb8d.json")
    firebase_admin.initialize_app(cred)
    return firestore.client()


db = get_db()
users_col = db.collection(u'users')
points_col = db.collection(u'points')


def auth(teamname, password):
    user = users_col.where(filter=FieldFilter(u'teamname', u'==', teamname)).where(
        filter=FieldFilter(u'password', u'==', password)).get()
    if user and user[0].exists: return user[0]


def add_points(user, points: int, level: int, tokens: int):
    user.reference.update({u'scores.' + str(level): {
        u'points': points,
        u'tokens': min(tokens, user.reference.get().to_dict()['scores'][str(level)]['tokens'])
    }})


def get_points(user):
    scores = user.reference.get().to_dict()['scores']
    return sum(score['points'] - score["tokens"] for score in scores.values())


if __name__ == '__main__':
    pass
