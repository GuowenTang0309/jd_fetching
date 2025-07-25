from fastapi import FastAPI
from typing import List
from models import JobSearchRequest, JobResult
from listing import fetch_job_listing_urls
from scraper import SeleniumJobScraper

app = FastAPI(title="LinkedIn Job Scraper API (v3)")

@app.post("/scrape", response_model=List[JobResult])
def scrape_jobs(req: JobSearchRequest):
    job_entries = fetch_job_listing_urls(req.job_title, req.location, req.pages)
    scraper = SeleniumJobScraper(headless=True)

    try:
        results: list[JobResult] = []
        for idx, entry in enumerate(job_entries, 1):
            job_title = entry["title"]
            job_company = entry["company"]
            job_location = entry["location"]
            job_url = entry["url"]

            try:
                desc, apply_url = scraper.fetch_detail(job_url)

                if desc is None or apply_url is None:
                    raise ValueError("Essential info missing")

                results.append(
                    JobResult(
                        title=job_title,
                        company=job_company,
                        location=job_location,
                        description=desc,
                        apply_url=apply_url,
                        failed=False
                    )
                )
                print(f"[{idx}/{len(job_entries)}] ✅ {job_title} | Apply: {apply_url}")

            except Exception as e:
                print(f"[{idx}/{len(job_entries)}] ❌ Failed: {job_url} | Reason: {e}")
                results.append(
                    JobResult(
                        title=job_title,
                        company=job_company,
                        location=job_location,
                        description="",
                        apply_url="",
                        failed=True
                    )
                )

        print(f"\n✅ Scrape finished: {len(results)} jobs processed")
        return results

    finally:
        scraper.close()
