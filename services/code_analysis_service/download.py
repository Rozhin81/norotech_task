import subprocess
import redis , asyncio
from fastapi import HTTPException

redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

async def download_repo(repo_url: str, job_id: str):
    repo_path = f"/repos/{job_id}"
    try:
        process = await asyncio.create_subprocess_exec(
            "git", "clone", repo_url, repo_path,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        await process.communicate()
        if process.returncode == 0:
            redis_client.set(job_id, repo_path)  
        else:
            redis_client.delete(job_id)
            raise HTTPException(status_code=500, detail="Failed to clone repository.")
    except Exception as e:
        redis_client.delete(job_id)
        raise HTTPException(status_code=500, detail=f"Error cloning repository: {str(e)}")