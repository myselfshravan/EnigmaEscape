import requests
import re
from typing import Dict, Any
from sentence_transformers import SentenceTransformer, util
import os
from .levels import Level


class GameValidator:
    API_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"
    forbids = [
        "replace",
        "swap",
        "change",
        "modify",
        "alter",
        "substitute",
    ]

    def __init__(self):
        self.valid_model = SentenceTransformer('paraphrase-distilroberta-base-v1')
        self.session = requests.Session()

    def validate_response(self, level: Level, prompt: str) -> Dict[str, Any]:
        """
        Validates a user's prompt for a given level and returns the response
        """
        # Check for forbidden words
        if any(w in prompt.lower() for w in self.forbids):
            return {
                "content": "I wont fall for that",
                "type": "warning"
            }

        # Check if prompt contains the target phrase
        if self._regex_validate(prompt, level.phrase):
            return {
                "content": "You cannot include the phrase in your question",
                "type": "error"
            }

        # Get AI response
        try:
            response = self._get_ai_response(prompt, level)
            content = response["choices"][0]["message"]["content"]

            # Validate if response matches target phrase
            if self._response_validate(content, level.phrase):
                return {
                    "content": content,
                    "type": "success",
                    "tokens": response["usage"]["prompt_tokens"]
                }

            return {
                "content": content,
                "type": "info"
            }
        except Exception as e:
            return {
                "content": f"Error processing request: {str(e)}",
                "type": "error"
            }

    def _get_ai_response(self, prompt: str, level: Level) -> Dict[str, Any]:
        """
        Gets response from the AI model
        """
        messages = [
            {
                "role": "system",
                "content": level.description
            },
            {
                "role": "user",
                "content": prompt
            }
        ]

        response = self.session.post(
            self.API_ENDPOINT,
            headers={"Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}"},
            json={
                "model": level.model,
                "messages": messages,
                "temperature": 0.5,
                "max_tokens": level.max_token
            }
        )
        return response.json()

    def _response_validate(self, response: str, target: str) -> bool:
        """
        Validates if the AI response matches the target phrase using sentence similarity
        """
        tokens_response = [w for w in re.split(r"[^a-zA-Z0-9]", response) if w]
        token_len = len([w for w in re.split(r'[^a-zA-Z0-9]', target) if w])
        embed_len = len(tokens_response) - token_len + 1

        embeds = self.valid_model.encode(
            [target] + [" ".join(tokens_response[i: i + token_len]) for i in range(embed_len)],
            convert_to_tensor=True
        )

        score = 0
        for i in range(embed_len):
            score = max(util.pytorch_cos_sim(embeds[0], embeds[i + 1]).item(), score)

        return score > 0.82

    def _regex_validate(self, prompt: str, target: str) -> bool:
        """
        Checks if the prompt contains any words from the target phrase
        """
        prompt_flat = re.sub(r'[^a-zA-Z0-9]', ' ', prompt).lower()
        for word in target.split():
            if bool(re.search(f"(^| ){word}( |$)", prompt_flat)):
                return True
        return False

    def __del__(self):
        if hasattr(self, 'session'):
            self.session.close()
