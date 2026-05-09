import json
import os
import requests

from router.config import MODEL_NAME, SYSTEM_PROMPT


class OpenAIRouter:
    def __init__(self) -> None:
        self.api_key = os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY 환경변수가 설정되지 않았습니다.")

        self.url = "https://api.openai.com/v1/responses"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

    def classify(self, text: str) -> str:
        payload = {
            "model": MODEL_NAME,
            "input": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": text},
            ],
            "max_output_tokens": 30,
        }

        response = requests.post(
            self.url,
            headers=self.headers,
            json=payload,
            timeout=30,
        )
        response.raise_for_status()

        data = response.json()

        raw = data.get("output_text", "").strip()

        if not raw:
            try:
                output = data.get("output", [])
                parts = []
                for item in output:
                    for content in item.get("content", []):
                        if content.get("type") == "output_text":
                            parts.append(content.get("text", ""))
                raw = "".join(parts).strip()
            except Exception:
                raw = ""

        try:
            parsed = json.loads(raw)
            label = parsed.get("label", "etc")
        except Exception:
            label = "etc"

        allowed = {"action", "location", "symptom", "mixed", "etc"}
        return label if label in allowed else "etc"
