# LinkedIn Job Scraper API

FastAPI service that searches LinkedIn jobs and scrapes full job details with Selenium.

---

## Features

| Capability | Details |
|------------|---------|
| **Search jobs** | Query by *job title*, *location*, and *pages* |
| **Scrape details** | Title · Company · Location · Description · Apply URL (external or **Easy Apply** marker) · Industry |
| **REST endpoint** | `POST /scrape` → JSON array of results |
| **Headless Selenium** | Chrome driven by **Chromedriver**; cookies kept in a dedicated profile |
| **Fallback logic** | Handles external redirects, new‑tab openings, and Easy Apply modals |

---
## Quick start

```bash
# 1  Install deps
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# 2  Run API
uvicorn main:app --reload
```

## Example Request

Send a **POST** request to `/scrape`:

curl -X POST http://127.0.0.1:8000/scrape  
  -H "Content-Type: application/json"  
  -d '{ "job_title": "Data analyst", "location": "San Francisco, CA", "pages": 1 }'
