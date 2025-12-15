import logging
import re
from collections import namedtuple
from difflib import SequenceMatcher
from typing import Union

import requests
import streamlit as st

logging.basicConfig(level=logging.DEBUG)

Level = namedtuple("Level", ["name", "description", "hint", "phrase"])


class EnigmaEscape:
    API_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"
    API_KEY = st.secrets["groq_api"]
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

    def _normalize_text(self, text: str) -> list[str]:
        """Lowercase and split on non-alphanumeric characters."""
        return [w.lower() for w in re.split(r'[^a-zA-Z0-9]', text) if w]

    def resp_validate(self, response: str):
        """
        Validate if the AI response matches the target phrase using
        normalization and fuzzy matching to avoid heavy embedding models.
        """
        response_words = self._normalize_text(response)
        target_words = self._normalize_text(self.level.phrase)

        response_text = ' '.join(response_words)
        target_text = ' '.join(target_words)

        # Exact normalized match
        if response_text == target_text:
            return True

        # Fuzzy whole-string similarity
        similarity = SequenceMatcher(None, response_text, target_text).ratio()

        # Sliding window comparison for close matches
        window_size = len(target_words)
        for i in range(len(response_words) - window_size + 1):
            window = ' '.join(response_words[i:i + window_size])
            if SequenceMatcher(None, window, target_text).ratio() > 0.85:
                return True

        return similarity > 0.85

    def regx_validate(self, que: str):
        que_flat = re.sub(r'[^a-zA-Z0-9]', ' ', que).lower()
        for word in self.level.phrase.split():
            if bool(re.search(f"(^| ){word}( |$)", que_flat)):
                return True
        return False


if __name__ == '__main__':
    pass
