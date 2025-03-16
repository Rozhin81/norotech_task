from pydantic import BaseModel


class AnalysisInput(BaseModel):
    repo_url: str

class AnalysisOutput(BaseModel):
    job_id: str

