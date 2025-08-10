import requests
import re
from typing import Dict, Any, List
import os
from difflib import SequenceMatcher
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

    def _normalize_text(self, text: str) -> List[str]:
        """
        Normalizes text by removing special characters and converting to lowercase
        """
        return [w.lower() for w in re.split(r'[^a-zA-Z0-9]', text) if w]

    def _response_validate(self, response: str, target: str) -> bool:
        """
        Validates if the AI response matches the target phrase using string similarity
        and word matching
        """
        # Normalize both strings
        response_words = self._normalize_text(response)
        target_words = self._normalize_text(target)

        # Direct word sequence match
        response_text = ' '.join(response_words)
        target_text = ' '.join(target_words)
        
        # Check for exact match first
        if response_text == target_text:
            return True

        # Use sequence matcher for fuzzy matching
        matcher = SequenceMatcher(None, response_text, target_text)
        similarity = matcher.ratio()

        # Look for the target phrase within a sliding window of the response
        window_size = len(target_words)
        for i in range(len(response_words) - window_size + 1):
            window = ' '.join(response_words[i:i + window_size])
            if SequenceMatcher(None, window, target_text).ratio() > 0.85:
                return True

        return similarity > 0.85

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
