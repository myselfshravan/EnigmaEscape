import requests
from typing import Union
import re
from collections import namedtuple
from sentence_transformers import SentenceTransformer, util
import streamlit as st

Level = namedtuple("Level", ["name", "description", "hint", "phrase"])


class EnigmaEscape:
    API_ENDPOINT = "https://api.endpoints.anyscale.com/v1/chat/completions"
    API_KEY = st.secrets["anyscale_api"]
    forbids = [
        "replace",
        "swap",
        "change",
        "modify",
        "alter",
        "substitute",
    ]

    def body(self, que: str):
        self.messages[-1] = {
            "role": "user",
            "content": que,
        }
        return {
            "model": self.level.model,
            "messages": self.messages,
            "temperature": 0.5,
            "max_tokens": self.level.max_token,
        }

    def __enter__(self):
        self.session = requests.Session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

    def __init__(self, levels: list[Level]):
        self.valid_model = SentenceTransformer('paraphrase-distilroberta-base-v1')
        self.levels = levels
        self.level = None
        self.messages = []
        self.session: Union["requests.Session", None] = None

    def set_level(self, lev: int):
        self.level = self.levels[lev]
        self.messages = [
            {
                "role": "system",
                "content": self.level.description,
            },
            {
                "role": "user",
                "content": "",
            },
        ]

    def chat(self, que: str):
        if any(w in que.lower() for w in self.forbids):
            return {
                "content": "I wont fall for that",
                "type": "warning",
            }
        if self.regx_validate(que):
            return {
                "content": "You cannot include the phrase in your question",
                "type": "error",
            }
        body = self.body(que)
        resp = self.session.post(
            self.API_ENDPOINT,
            headers={"Authorization": f"Bearer {self.API_KEY}"},
            json=body
        ).json()
        content = resp["choices"][0]["message"]["content"]
        if self.resp_validate(content):
            return {
                "content": content,
                "type": "success",
                "tokens": resp["usage"]["prompt_tokens"],
            }
        return {
            "content": content,
            "type": "info",
        }

    def resp_validate(self, que: str):
        tokens_que = [w for w in re.split(r"[^a-zA-Z0-9]", que) if w]
        token_len = len([w for w in re.split(r'[^a-zA-Z0-9]', self.level.phrase) if w])
        embed_len = len(tokens_que) - token_len + 1
        embeds = self.valid_model.encode(
            [self.level.phrase] + [" ".join(tokens_que[i: i + token_len]) for i in range(embed_len)],
            convert_to_tensor=True
        )
        score = 0
        for i in range(embed_len):
            score = max(util.pytorch_cos_sim(embeds[0], embeds[i + 1]).item(), score)
            # print(score, " ".join(tokens_que[i: i + token_len]), self.level.phrase, sep=" | ")
        return score > 0.82

    def regx_validate(self, que: str):
        que_flat = re.sub(r'[^a-zA-Z0-9]', ' ', que).lower()
        for word in self.level.phrase.split():
            if bool(re.search(f"(^| ){word}( |$)", que_flat)):
                return True
        return False


if __name__ == '__main__':
    pass
