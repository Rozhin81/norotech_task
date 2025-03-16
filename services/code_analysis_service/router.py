from fastapi import FastAPI , HTTPException
from download import download_repo
import uvicorn
import uuid , redis
from schemas import *

app = FastAPI()
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

@app.post("/analyze/start", response_model=AnalysisOutput)
async def start_analysis(input_data: AnalysisInput):
    job_id = str(uuid.uuid4())
    await download_repo(input_data.repo_url, job_id)
    return {"job_id": job_id}




if __name__ == "__main__":
    uvicorn.run(app='router:app', host='localhost', port=8001, reload=True)
