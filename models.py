from pydantic import BaseModel, Field
from typing import Optional, List

class JobSearchRequest(BaseModel):
    job_title: str = Field(...)
    location: str   = Field(...)
    #time_span (e.g. "last 24 hours", "last week")
    #website (e.g. Linkedin, Handshake, or Indeed)
    pages: int = Field(1, ge=1, le=5, example=2,
                       description="How many result pages")

class JobResult(BaseModel):
    title: str
    company: str
    location: str
    description: str = ""      # filled by scraper
    apply_url: str = ""        # filled by scraper
    failed: bool = False       # for robustness 
