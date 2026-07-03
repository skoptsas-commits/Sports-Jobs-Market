#!/usr/bin/env python3
"""
Fetch a live snapshot of sports data/science job postings from the Adzuna API.

Used under Adzuna's "Personal or academic research" permitted use
(see https://developer.adzuna.com/docs/terms_of_service). Output is
aggregate counts and sampled salary stats only — no full job
descriptions are stored or redistributed, per ToS obligations.

Matching strategy: Adzuna's `what` param requires all words to appear
(phrase/AND-like matching), which under-counts niche multi-word roles
(e.g. "motorsport data engineer" often returns 0 even though relevant
jobs exist under slightly different wording). To keep counts honest
without inflating them, each query first tries `what` (precise), and
only falls back to `what_or` (any word matches) if that returns zero
results. The output records which matching mode was actually used
(`match_type`) so the dashboard can be transparent about it instead of
silently implying a 0 count means "no demand".

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
# Kept to 1-2 words where possible so Adzuna's default AND-style `what` matching
# still finds real postings (3+ word phrases were returning 0 far too often).
QUERIES = [
    {"keyword": "sports data scientist", "country": "us"},
    {"keyword": "sports scientist football", "country": "gb"},
    {"keyword": "sports analyst", "country": "gb"},
    {"keyword": "performance analyst", "country": "gb"},
    {"keyword": "motorsport engineer", "country": "gb"},
    {"keyword": "cycling analyst", "country": "gb"},
    {"keyword": "basketball analyst", "country": "us"},
]

BASE_URL = "https://api.adzuna.com/v1/api/jobs/{country}/search/1"


def call_adzuna(keyword: str, country: str, param_name: str) -> dict:
    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "results_per_page": 20,
        param_name: keyword,
        "content-type": "application/json",
    }
    url = f"{BASE_URL.format(country=country)}?{urlencode(params)}"
    req = Request(url, headers={"User-Agent": "sports-jobs-market-analyzer/1.0 (personal research)"})
    with urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))


def fetch_query(keyword: str, country: str) -> dict:
    # Try precise (AND / phrase-like) matching first.
    payload = call_adzuna(keyword, country, "what")
    match_type = "precise (all words)"

    if not payload.get("count"):
        # Fall back to OR matching so a niche multi-word phrase doesn't
        # falsely read as "zero demand" when it's really a matching artifact.
        time.sleep(2)
        payload = call_adzuna(keyword, country, "what_or")
        match_type = "broad (any word)"

    results = payload.get("results", [])
    salaries_min = [r["salary_min"] for r in results if r.get("salary_min")]
    salaries_max = [r["salary_max"] for r in results if r.get("salary_max")]

    return {
        "keyword": keyword,
        "country": country,
        "count": payload.get("count", 0),
        "match_type": match_type,
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
            print(f"OK   {q['country']}/{q['keyword']}: {result['count']} postings ({result['match_type']})")
        except Exception as e:
            print(f"FAIL {q['country']}/{q['keyword']}: {e}", file=sys.stderr)
            snapshot["queries"].append({
                "keyword": q["keyword"],
                "country": q["country"],
                "count": None,
                "match_type": "error",
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
