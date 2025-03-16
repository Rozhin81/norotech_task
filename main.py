import os
import requests
from fastapi import FastAPI, HTTPException
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import uvicorn
from services.openai_service.code_review import CodeReviewAssistant
from services.deepseek_service.code_review import DeepSeekCodeReviewAssistant
from services.llm_hosting.local_connection import generator

app = FastAPI()

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")


@app.post("/analyze")
def analyze_function(data:dict):
    """Receives function code and forwards it to the appropriate LLM."""
    function_code = data["function_code"]
    if LLM_PROVIDER == "openai":
        openai_object = CodeReviewAssistant()
        return openai_object.analyze_function(function_code = function_code)
    elif LLM_PROVIDER == "deepseek":
        deepseek_object = DeepSeekCodeReviewAssistant()
        return deepseek_object.analyze_function(function_code = function_code)
    elif LLM_PROVIDER == "local":
        return generator(function_code)
    else:
        raise HTTPException(status_code=400, detail="Invalid LLM provider")


if __name__ == "__main__":
    uvicorn.run(app='test:app', host='localhost', port=8008, reload=True)
