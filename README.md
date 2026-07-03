# Sports Jobs Market Analyzer

Snapshot dashboard of the sports data/science jobs market — Data Scientist, Sports Scientist, Performance & Data Analyst roles across football, basketball (NBA), Formula 1, MotoGP and WorldTour cycling teams.

**Author:** Stelios Koptsas
**Live demo:** enable GitHub Pages (see below) → `https://<your-username>.github.io/sports-jobs-market-analyzer/`

## What it shows

- Typical salary ranges by sport/role
- Cross-sport skill & tool footprint (Python, SQL, R, Power BI/Tableau, ML frameworks, sport-specific platforms)
- Role table: core responsibilities, tools, education path, typical salary — by sport
- UK football analyst pay by tier
- Snapshot of which employers had the most open analytics roles (May 2026)

Built with [Chart.js](https://www.chartjs.org/) and [Grid.js](https://gridjs.io/), no backend — single static `index.html`.

## Data sources

This is a research snapshot (July 2026), not a live feed — LinkedIn and most club career sites block automated scraping, and no job-board API is connected. Figures were compiled from public job postings and market/salary research:

**Football**
- [Jobs In Football — Data Science](https://jobsinfootball.com/categories/data-science/)
- [Jobs In Football — Sports Science](https://jobsinfootball.com/categories/sports-science/)
- [Learning People — Football data jobs & pay](https://www.learningpeople.com/uk/resources/blog/football-data-jobs/)
- [Analytics Sports Jobs — Football analyst salary UK 2026](https://analyticssportsjobs.com/blog/premier-league-analyst-salary)

**Basketball (NBA)**
- [TeamWork Online — LA Lakers Data Scientist posting](https://www.teamworkonline.com/basketball-jobs/los-angeles-lakers/los-angeles-lakers-jobs/data-scientist-2169726)
- ZipRecruiter NBA Analytics salary data (aggregated, June 2026)

**Formula 1**
- [Aston Martin F1 — So you want to be an F1 data engineer?](https://www.astonmartinf1.com/en-GB/news/feature/so-you-want-to-be-an-f1-data-engineer)
- [Fluid Jobs — F1/Motorsport Data Science listings](https://fluidjobs.com/jobs/data-scientist-jobs)
- [Trackside Careers — Data Science in Motorsport](https://tracksidecareers.com/blog/sports-data-science-jobs)

**MotoGP**
- [MotoGP.com — What is the role of a MotoGP Race Engineer?](https://www.motogp.com/en/news/2025/04/07/what-is-the-role-of-a-motogp-race-engineerx/1062790)

**Cycling (WorldTour)**
- [TeamWork.net — Data & Performance: TeamWork supports INEOS Grenadiers](https://www.teamwork.net/en/data-performance-teamwork-ineos-grenadiers/)
- Indeed / ZipRecruiter cycling data analyst listings (aggregated)

**Market size & hiring trends**
- [Grand View Research — Sports Analytics Market Size Report](https://www.grandviewresearch.com/industry-analysis/sports-analytics-market)
- [Research.com — 2026 Sports Analytics Careers Outlook](https://research.com/advice/sports-analytics-careers-skills-education-salary-job-outlook)
- [Analytics Sports Jobs — Top hiring companies 2026](https://analyticssportsjobs.com/blog/companies-hiring-most-sports-analysts-2026)
- [ZipRecruiter — Sports Data Analyst Salary](https://www.ziprecruiter.com/Salaries/Sports-Data-Analyst-Salary)

Salary figures are aggregator ranges spanning junior→senior levels, not single-source exact figures — treat as directional, not precise.

## Publishing this as your own GitHub project

1. Create a new empty repo on GitHub (no README/license, so it doesn't conflict): `sports-jobs-market-analyzer`.
2. On your machine, in the folder with `index.html` and this `README.md`:

```bash
git init
git config user.name "Stelios Koptsas"
git config user.email "s.koptsas@gmail.com"
git add .
git commit -m "Initial commit: sports jobs market analyzer dashboard"
git branch -M main
git remote add origin https://github.com/<your-username>/sports-jobs-market-analyzer.git
git push -u origin main
```

3. In the repo on GitHub: **Settings → Pages → Source: `main` branch, `/ (root)`** → Save. After a minute your dashboard is live at `https://<your-username>.github.io/sports-jobs-market-analyzer/`.

Since you run these commands yourself (with your own git config and GitHub login), the commit history and repo are authored under your account.

## Next steps / ideas

- Refresh the snapshot periodically (ask Claude to re-run the research) and commit updated numbers.
- Add more sports (tennis, esports, Olympic federations).
- Turn the static table into a small CSV you version alongside the page, so changes are diffable.
