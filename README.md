# Sports Jobs Market Analyzer

Snapshot dashboard of the sports data/science jobs market — Data Scientist, Sports Scientist, Performance & Data Analyst roles across football, basketball (NBA), Formula 1, MotoGP and WorldTour cycling teams.

**Author:** Stelios Koptsas
**Live demo:** `https://skoptsas-commits.github.io/Sports-Jobs-Market/`

## What it shows

- Typical salary ranges by sport/role
- Cross-sport skill & tool footprint (Python, SQL, R, Power BI/Tableau, ML frameworks, sport-specific platforms)
- Role table: core responsibilities, tools, education path, typical salary — by sport
- UK football analyst pay by tier
- Snapshot of which employers had the most open analytics roles
- **Live job postings snapshot** — real, current counts pulled from the Adzuna Jobs API (see below)

Built with [Chart.js](https://www.chartjs.org/) and [Grid.js](https://gridjs.io/), no backend — single static `index.html`.

## Two update mechanisms (run independently)

**1. Search-based snapshot (KPI cards, salary/skill charts, role table)**
Refreshed periodically via an AI research pass (web search across job boards, salary aggregators and market reports), then committed to `index.html` directly. This is qualitative/aggregated analysis, not a raw feed.

**2. Live Adzuna postings (bottom card)**
A GitHub Actions workflow (`.github/workflows/adzuna-refresh.yml`) runs every Monday at 09:00 UTC (or on-demand via the Actions tab → "Run workflow"):
- `scripts/fetch_adzuna.py` calls the [Adzuna Jobs API](https://developer.adzuna.com/) for a curated set of sport/role keywords across GB/US
- Writes aggregate counts + sampled average salaries to `data/adzuna_snapshot.json` (no full job descriptions are stored, per Adzuna's ToS)
- Commits the updated JSON automatically using the workflow's built-in `GITHUB_TOKEN` — no manual push needed
- `index.html` fetches this JSON client-side at page load and renders it live

### Required setup for the live feed

1. Get free API credentials at [developer.adzuna.com](https://developer.adzuna.com/) (`app_id` + `app_key`).
2. In this repo: **Settings → Secrets and variables → Actions → New repository secret**, add:
   - `ADZUNA_APP_ID`
   - `ADZUNA_APP_KEY`
3. Confirm Actions is enabled: **Settings → Actions → General → Allow all actions**.
4. Trigger it once manually: **Actions tab → "Refresh Adzuna job market snapshot" → Run workflow**, so `data/adzuna_snapshot.json` exists before the first Monday.

**Adzuna usage terms:** used under the "Personal or academic research" permitted use in their [ToS](https://developer.adzuna.com/docs/terms_of_service) — attribution to "The Adzuna API" is included on the page and required. Default rate limits (25/min, 250/day) comfortably cover the ~7 weekly queries this script makes.

**Query matching:** Adzuna's `what` param requires all words in a keyword to appear (phrase/AND-like), which under-counts niche multi-word roles. Each query tries `what` first; if that returns 0, it automatically retries with `what_or` (any word matches) as a fallback. The dashboard table shows a **Match** column (`exact` vs `broad*`) so a 0-turned-broad result is never silently presented as precise.

## Data sources (search-based snapshot)

This is a research snapshot (refreshed 3 Jul 2026), not a live LinkedIn feed — LinkedIn and most club career sites block automated scraping, and no LinkedIn API is connected. Figures were compiled from public job postings and market/salary research:

**Football**
- [Jobs In Football — Data Science](https://jobsinfootball.com/categories/data-science/)
- [Jobs In Football — Sports Science](https://jobsinfootball.com/categories/sports-science/)
- [ZipRecruiter — Football Data Science Jobs](https://www.ziprecruiter.com/Jobs/Football-Data-Science)
- [CASES — Football Data Scientist posting](https://www.cases.org.uk/advert-football_data_scientist.html)
- [Catapult One — Sports science and football](https://one.catapultsports.com/blog/sports-science-and-football/)

**Basketball (NBA)**
- [ZipRecruiter — NBA Analytics salary](https://www.ziprecruiter.com/Jobs/Nba-Analytics)
- [TeamWork Online — LA Lakers Data Scientist posting](https://www.teamworkonline.com/basketball-jobs/los-angeles-lakers/los-angeles-lakers-jobs/data-scientist-2169726)

**Formula 1**
- [Aston Martin F1 — So you want to be an F1 data engineer?](https://www.astonmartinf1.com/en-GB/news/feature/so-you-want-to-be-an-f1-data-engineer)
- [ZipRecruiter — Formula 1 Data Science Jobs](https://www.ziprecruiter.com/Jobs/Formula-1-Data-Science)
- [Fluid Jobs — F1/Motorsport Data Science listings](https://fluidjobs.com/jobs/data-scientist-jobs)

**MotoGP**
- [MotoGP.com — What is the role of a MotoGP Race Engineer?](https://www.motogp.com/en/news/2025/04/07/what-is-the-role-of-a-motogp-race-engineerx/1062790)
- [Trackside Careers — Performance Engineer Jobs in Motorsport](https://tracksidecareers.com/blog/performance-engineer-jobs)

**Cycling (WorldTour)**
- [TeamWork.net — Data & Performance: TeamWork supports INEOS Grenadiers](https://www.teamwork.net/en/data-performance-teamwork-ineos-grenadiers/)
- [ZipRecruiter — Cycling Data Analyst Jobs](https://www.ziprecruiter.com/Jobs/Cycling-Data-Analyst)

**Market size & hiring trends**
- [Grand View Research — Sports Analytics Market Size Report](https://www.grandviewresearch.com/industry-analysis/sports-analytics-market)
- [Research.com — 2026 Sports Analytics Careers Outlook](https://research.com/advice/sports-analytics-careers-skills-education-salary-job-outlook)
- [Analytics Sports Jobs — Top hiring companies 2026](https://analyticssportsjobs.com/blog/companies-hiring-most-sports-analysts-2026)
- [ZipRecruiter — Sports Data Analyst Salary](https://www.ziprecruiter.com/Salaries/Sports-Data-Analyst-Salary)
- [The Adzuna API](http://www.adzuna.co.uk/) — live postings data (see above)

Salary figures in the snapshot sections are aggregator ranges spanning junior→senior levels, not single-source exact figures — treat as directional, not precise.

## Publishing / project structure

```
index.html                          # the dashboard (static, self-contained)
README.md
scripts/fetch_adzuna.py             # pulls live Adzuna data
data/adzuna_snapshot.json           # generated by the workflow, do not hand-edit
.github/workflows/adzuna-refresh.yml
```

Repo: `github.com/skoptsas-commits/Sports-Jobs-Market`, GitHub Pages served from `main` / root.

## Next steps / ideas

- Add more sports (tennis, esports, Olympic federations) to both the snapshot and the Adzuna query list.
- Expand Adzuna queries to more countries (currently GB/US only).
- Turn the snapshot table into a small versioned CSV so changes are diffable over time.
