import json
import requests
import os
from response_schema import CodeReviewResponseFormat
from dotenv import load_dotenv
load_dotenv()


class DeepSeekCodeReviewAssistant:
    def __init__(self, temperature=0.7):
        self.api_key = os.getenv("DEEPSEEK_APIKEY")

        if not self.api_key:
            raise ValueError("DeepSeek API Key is missing! Set 'DEEPSEEK_APIKEY' in your .env file.")

        self.temperature = temperature
        self.api_url = "https://api.deepseek.com/v1/chat/completions"  # DeepSeek API endpoint
        self.system_prompt = (
            "You are an advanced code review assistant. Your task is to analyze the given Python function and provide structured feedback "
            "on how to improve its readability, efficiency, and best practices. "
            "Your response should be in JSON format with the following fields: "
            "- \"suggestions\": A list of recommendations to improve the function. "
            "- \"issues\": A list of potential issues found in the function. "
            "Ensure that the response follows this exact JSON format."
        )

    def analyze_function(self, function_code):
        """Sends the function code to DeepSeek's API for analysis and retrieves structured suggestions."""

        user_prompt = f"Analyze the following Python function and provide improvement suggestions:\n\n```python\n{function_code}\n```"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "deepseek-coder",  # DeepSeek code analysis model
            "temperature": self.temperature,
            "messages": [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "response_format": {
                "type": "json_schema",
                "json_schema": CodeReviewResponseFormat.model_json_schema()
            }
        }

        # Send request to DeepSeek API
        response = requests.post(self.api_url, headers=headers, json=payload)

        if response.status_code != 200:
            raise ValueError(f"DeepSeek API Error: {response.status_code} - {response.text}")

        # Extract and parse the structured JSON response
        response_data = response.json()
        response_content = response_data["choices"][0]["message"]["content"]

        # Validate the response using Pydantic
        json_response = json.loads(response_content)
        return CodeReviewResponseFormat(**json_response).dict()
