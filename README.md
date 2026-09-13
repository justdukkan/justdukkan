# justdukkan.com

Source of [justdukkan.com](https://justdukkan.com) — JustDukkan, LLC. AI solutions architecture: process automation, system design and agentic systems.

Static site, no build step.

- `index.html` — English (default), `tr/index.html` — Turkish
- `insights/` — articles, generated from `tools/articles.py` with `python3 tools/build_insights.py`
- `assets/` — stylesheet, interactive orchestrator demo (`demo.js`), wordmark and icons
- `llms.txt`, `robots.txt`, `sitemap.xml` — discoverability for search engines and AI crawlers

Deployed on Vercel from `main`.
