import requests
import pandas as pd
import os
import time
from dotenv import load_dotenv

load_dotenv()

API_ID = os.getenv("ADZUNA_APP_ID")
API_KEY = os.getenv("ADZUNA_APP_KEY")

BASE_URL = "https://api.adzuna.com/v1/api/jobs/gb/search/1"

SEARCH_TERMS = [
    "data analyst",
    "data scientist",
    "data engineer",
    "machine learning engineer",
    "business analyst",
    "python developer",
    "software engineer",
    "power bi developer"
]

def fetch_jobs(search_term, pages=3):
    all_jobs = []
    
    for page in range(1, pages + 1):
        url = BASE_URL.format(page=page)
        params = {
            "app_id": API_ID,
            "app_key": API_KEY,
            "results_per_page": 50,
            "what": search_term,
            "content-type": "application/json"
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            jobs = data.get("results", [])

            for job in jobs:
                all_jobs.append({
                    "title": job.get("title", ""),
                    "company": job.get("company", {}).get("display_name"),
                    "location": job.get("location", {}).get("display_name"),
                    "category": job.get("category", {}).get("label", ""),
                    "salary_min": job.get("salary_min", None),
                    "salary_max": job.get("salary_max", None),
                    "contract_type": job.get("contract_type", ""),
                    "created": job.get("created", ""),
                    "description": job.get("description", ""),
                    "redirect_url": job.get("redirect_url", ""),
                    "search_term": search_term
                })

            print(f"Fetched page {page} for '{search_term}' - {len(jobs)} jobs")
            time.sleep(1)  

        except Exception as e:
            print(f"Error on page {page} for '{search_term}': {e}")

    return all_jobs

def main():
    all_jobs = []
    
    for term in SEARCH_TERMS:
        print(f"\nFetching: {term}")
        jobs = fetch_jobs(term, pages=3)
        all_jobs.extend(jobs)
        time.sleep(2)

    df = pd.DataFrame(all_jobs)
    df.drop_duplicates(subset=["title", "company", "location"], inplace=True)
    df.reset_index(drop=True, inplace=True)

    output_path = os.path.join("data", "raw_jobs.csv")
    df.to_csv(output_path, index=False)

    print(f"\nDone! Total jobs collected: {len(df)}")
    print(f"Saved to: {output_path}")
    print(df.head())

if __name__ == "__main__":
    main()