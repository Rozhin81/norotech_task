from pydantic import BaseModel
from typing import List

class CodeReviewResponseFormat(BaseModel):
    suggestions: List[str] 
    issues: List[str]