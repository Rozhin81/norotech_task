from pydantic import BaseModel

class CodeInput(BaseModel):
    function_code : str

class AnalysisOutput(BaseModel) :
    suggestions: list[str]