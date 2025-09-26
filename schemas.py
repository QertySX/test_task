from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from typing import Dict
from datetime import datetime


class JobResponse(BaseModel):
    job_id: str 
    title: Optional[str]
    filename: str
    pages: int 
    status: str
    created_at: datetime
    updated_at: datetime

