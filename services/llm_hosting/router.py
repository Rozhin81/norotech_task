from fastapi import FastAPI
from schemas import CodeInput ,  AnalysisOutput
from services.llm_hosting.analyzation import Analyze
import uvicorn
 
app = FastAPI()


@app.post("/analyze", response_model=AnalysisOutput)
def analyze_function_code(input_data: CodeInput):
    analyze = Analyze(input_data.function_code)
    suggestions = analyze.analyze_code()
    return {"suggestions": suggestions}



if __name__ == "__main__":
    uvicorn.run(app='router:app', host='localhost', port=8000, reload=True)
