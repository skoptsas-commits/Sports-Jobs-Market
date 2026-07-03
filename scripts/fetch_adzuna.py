#!/usr/bin/env python3
"""
Fetch a live snapshot of sports data/science job postings from the Adzuna API.

Used under Adzuna's "Personal or academic research" permitted use
(see https://developer.adzuna.com/docs/terms_of_service). Output is
aggregate counts and sampled salary stats only — no full job
descriptions are stored or redistributed, per ToS obligations.

Requires env vars: ADZUNA_APP_ID, ADZUNA_APP_KEY
Writes: data/adzuna_snapshot.json
"""
import json
import os
import sys
import time
from datetime import datetime, timezone
from urllib.request import urlopen, Request
from urllib.parse import urlencode

APP_ID = os.environ.get("ADZUNA_APP_ID")
APP_KEY = os.environ.get("ADZUNA_APP_KEY")

if not APP_ID or not APP_KEY:
    print("ERROR: ADZUNA_APP_ID / ADZUNA_APP_KEY environment variables are required.", file=sys.stderr)
    sys.exit(1)

# Curated keyword x country combinations covering the sports covered by the dashboard.
QUERIES = [
    {"keyword": "sports data analyst", "country": "gb"},
    {"keyword": "sports data scientist", "country": "us"},
    {"keyword": "sports scientist football", "country": "gb"},
    {"keyword": "performance analyst football", "country": "gb"},
    {"keyword": "motorsport data engineer", "country": "gb"},
    {"keyword": "cycling performance analyst", "country": "gb"},
    {"keyword": "basketball data analyst", "country": "us"},
]

BASE_URL = "https://api.adzuna.com/v1/api/jobs/{country}/search/1"


def fetch_query(keyword: str, country: str) -> dict:
    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "results_per_page": 20,
        "what": keyword,
        "content-type": "application/json",
    }
    url = f"{BASE_URL.format(country=country)}?{urlencode(params)}"
    req = Request(url, headers={"User-Agent": "sports-jobs-market-analyzer/1.0 (personal research)"})
    with urlopen(req, timeout=20) as resp:
        payload = json.loads(resp.read().decode("utf-8"))

    results = payload.get("results", [])
    salaries_min = [r["salary_min"] for r in results if r.get("salary_min")]
    salaries_max = [r["salary_max"] for r in results if r.get("salary_max")]

    return {
        "keyword": keyword,
        "country": country,
        "count": payload.get("count", 0),
        "sample_size": len(results),
        "avg_salary_min": round(sum(salaries_min) / len(salaries_min), 0) if salaries_min else None,
        "avg_salary_max": round(sum(salaries_max) / len(salaries_max), 0) if salaries_max else None,
    }


def main():
    snapshot = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": "The Adzuna API",
        "attribution_url": "http://www.adzuna.co.uk/",
        "queries": [],
    }

    for q in QUERIES:
        try:
            result = fetch_query(q["keyword"], q["country"])
            snapshot["queries"].append(result)
            print(f"OK   {q['country']}/{q['keyword']}: {result['count']} postings")
        except Exception as e:
            print(f"FAIL {q['country']}/{q['keyword']}: {e}", file=sys.stderr)
            snapshot["queries"].append({
                "keyword": q["keyword"],
                "country": q["country"],
                "count": None,
                "sample_size": 0,
                "avg_salary_min": None,
                "avg_salary_max": None,
                "error": str(e),
            })
        time.sleep(3)  # stay well within the 25 hits/min limit

    os.makedirs("data", exist_ok=True)
    with open("data/adzuna_snapshot.json", "w") as f:
        json.dump(snapshot, f, indent=2)

    print("Wrote data/adzuna_snapshot.json")


if __name__ == "__main__":
    main()
