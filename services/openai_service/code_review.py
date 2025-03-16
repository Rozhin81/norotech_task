import json
import openai
import os
from response_schema import CodeReviewResponseFormat
from dotenv import load_dotenv
load_dotenv()


class CodeReviewAssistant:
    def __init__(self, temperature=0.7):
        self.api_key = str(os.getenv("OPENAI_APIKEY"))
        print(self.api_key)
        self.client = openai.OpenAI(api_key=self.api_key)
        self.temperature = temperature
        self.system_prompt = (
            "You are an advanced code review assistant. Your task is to analyze the given Python function and provide structured feedback "
            "on how to improve its readability, efficiency, and best practices. "
            "Your response should be in JSON format with the following fields: "
            "- \"suggestions\": A list of recommendations to improve the function. "
            "- \"issues\": A list of potential issues found in the function. "
            "Ensure that the response follows this exact JSON format."
        )

    def analyze_function(self, function_code):
        """Sends the function code to OpenAI's API for analysis and retrieves structured suggestions."""

        user_prompt = f"Analyze the following Python function and provide improvement suggestions:\n\n```python\n{function_code}\n```"

        response = self.client.chat.completions.create(
            model="gpt-4o",  
            temperature=self.temperature,
            messages=[
                {
                    "role": "system",
                    "content": self.system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {
                "name": "code_review",
                "schema": CodeReviewResponseFormat.model_json_schema()
                }
            }
        )

        # Extract the structured JSON response
        response_content = response.choices[0].message.content
        json_response = json.loads(response_content)
        return json_response