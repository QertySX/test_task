from fastapi import APIRouter, UploadFile, File, HTTPException
from uuid import uuid4
from datetime import datetime
import os 
from pypdf import PdfReader
from schemas import JobResponse


router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

jobs = dict()

@router.post('/jobs')
async def create_job(file: UploadFile = File(...), title: str = None):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=415, detail='неправильний MIME/type')

    contents = await file.read()
    if len(contents) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="більше 10мб не приймаєтся")   

    job_id = str(uuid4())    
    filename = file.filename
    file_path = os.path.join(UPLOAD_DIR, job_id + ".pdf")

    with open(file_path, "wb") as f:
        f.write(contents)

    try:
        reader = PdfReader(file_path)
        pages = len(reader.pages)
    except:
        pages = 0
    
    now = datetime.utcnow()

    job = JobResponse(
        job_id=job_id,
        title=title,
        filename=filename,
        pages=pages,
        status="queued",
        created_at=now,
        updated_at=now,
    )

    jobs[job_id] = job.dict()

    return job


@router.get('/jobs')
async def get_job_status(status: str = None):
    if status:
        filtered_by_status_jobs = [job for job in jobs.values() if job["status"] == status]
        return filtered_by_status_jobs
    return list(jobs.values())
    

@router.get('/jobs/{id}')
async def get_job_id(job_id: str):
    filtred_by_id_jobs = [job for job in jobs.values() if job['job_id'] == job_id]
    return filtred_by_id_jobs