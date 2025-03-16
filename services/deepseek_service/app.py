from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from services.openai_service.code_review import CodeReviewAssistant

app = FastAPI()
review_assistant = CodeReviewAssistant()

class CodeReviewRequest(BaseModel):
    function_code: str

@app.post("/analyze")
def analyze_function(request: CodeReviewRequest):
    try:
        result = review_assistant.analyze_function(request.function_code)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))