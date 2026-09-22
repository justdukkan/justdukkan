#!/usr/bin/env python3
"""Generate /insights pages from articles.py. Run: python3 tools/build_insights.py"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from articles import ARTICLES  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), '..')
SITE = 'https://justdukkan.com'
DATE = '2026-09-22'          # last site-wide update (dateModified)
PUBLISHED = '2026-09-13'     # default first-publication date; per-article 'date' overrides

THEME_JS = '''  <script>
    (function () { var k = "jd-theme"; try { var t = localStorage.getItem(k); if (t) document.documentElement.setAttribute("data-theme", t); } catch (e) {}
      window.jdTheme = { current: function () { return document.documentElement.getAttribute("data-theme") || (matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light"); },
        toggle: function () { var n = jdTheme.current() === "dark" ? "light" : "dark"; document.documentElement.setAttribute("data-theme", n); try { localStorage.setItem(k, n); } catch (e) {}
          var el = document.getElementById("cal-inline"); if (el && window.Cal && Cal.ns && Cal.ns.consultation) { Cal.ns.consultation("ui", { theme: n }); el.innerHTML = ""; Cal.ns.consultation("inline", { elementOrSelector: "#cal-inline", calLink: "justdukkan/solution-consultation", config: { layout: "month_view", theme: n } }); } } }; })();
  </script>
'''

CAL_SNIPPET = '''  <script>
    (function (C, A, L) { let p = function (a, ar) { a.q.push(ar); }; let d = C.document; C.Cal = C.Cal || function () { let cal = C.Cal; let ar = arguments; if (!cal.loaded) { cal.ns = {}; cal.q = cal.q || []; d.head.appendChild(d.createElement("script")).src = A; cal.loaded = true; } if (ar[0] === L) { const api = function () { p(api, arguments); }; const namespace = ar[1]; api.q = api.q || []; if (typeof namespace === "string") { cal.ns[namespace] = cal.ns[namespace] || api; p(cal.ns[namespace], ar); p(cal, ["initNamespace", namespace]); } else p(cal, ar); return; } p(cal, ar); }; })(window, "https://app.cal.com/embed/embed.js", "init");
    Cal("init", "consultation", { origin: "https://app.cal.com" });
    Cal.ns.consultation("ui", { theme: jdTheme.current(), hideEventTypeDetails: false, layout: "month_view" });
  </script>
'''


def header(active=''):
    return f'''  <header class="site-header">
    <div class="container">
      <a href="/" class="brand" aria-label="JustDukkan home">
        <span class="wordmark" role="img" aria-label="justdukkan"></span>
      </a>
      <nav class="nav-links" aria-label="Primary">
        <a href="/#services">Services</a>
        <a href="/#expertise">Expertise</a>
        <a href="/#approach">Approach</a>
        <a href="/insights/"{' aria-current="page"' if active == 'insights' else ''}>Insights</a>
        <a href="/#contact">Contact</a>
      </nav>
      <div class="nav-right">
        <button class="theme-toggle" type="button" onclick="jdTheme.toggle()" aria-label="Toggle light/dark theme">
          <svg class="i-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>
          <svg class="i-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>
        </button>
        <div class="lang" aria-label="Language">
          <a href="/" class="active" hreflang="en">EN</a>
          <span aria-hidden="true">/</span>
          <a href="/tr/" hreflang="tr" lang="tr">TR</a>
        </div>
        <a href="mailto:enes@justdukkan.com?subject=Solution%20consultation" class="btn btn-primary btn-sm">Get in touch <span class="arrow">→</span></a>
      </div>
    </div>
  </header>
'''


FOOTER = '''  <footer class="site-footer">
    <div class="container">
      <div class="footer-top">
        <a href="/" class="brand">
          <span class="wordmark" role="img" aria-label="justdukkan"></span>
        </a>
        <div class="lang">
          <a href="/" class="active" hreflang="en" lang="en">EN</a>
          <span aria-hidden="true">/</span>
          <a href="/tr/" hreflang="tr" lang="tr">TR</a>
        </div>
      </div>
      <div class="footer-grid">
        <div>
          <span class="footer-h">Company</span>
          <p>JustDukkan, LLC<br>1111B S Governors Ave, Suite 46654<br>Dover, DE 19904, USA<br>EIN 38-4388070</p>
        </div>
        <div>
          <span class="footer-h">Contact</span>
          <p><a href="mailto:enes@justdukkan.com">enes@justdukkan.com</a><br><a href="tel:+19106799657">+1 (910) 679-9657</a><br><a href="https://wa.me/19106799657" target="_blank" rel="noopener">WhatsApp</a></p>
        </div>
        <div>
          <span class="footer-h">Insights</span>
          <p>''' + '<br>'.join(f'<a href="/insights/{a["slug"]}/">{a["short"]}</a>' for a in ARTICLES[:4]) + '<br><a href="/insights/">All insights</a>' + '''</p>
        </div>
      </div>
      <div class="footer-bottom">© 2026 JustDukkan, LLC · <a href="/privacy/">Privacy</a></div>
    </div>
  </footer>
'''


def head(title, desc, url, ld):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{url}">
  <meta property="og:type" content="article">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{url}">
  <meta property="og:site_name" content="JustDukkan">
  <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
  <meta name="theme-color" content="#f7f7f4" media="(prefers-color-scheme: light)">
  <meta name="theme-color" content="#14120b" media="(prefers-color-scheme: dark)">
{THEME_JS}  <link rel="icon" href="/assets/favicon.svg?v=2" type="image/svg+xml">
  <link rel="icon" href="/assets/favicon-32.png?v=2" type="image/png" sizes="32x32">
  <link rel="apple-touch-icon" href="/assets/apple-touch-icon.png?v=2">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
  <script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=2)}
  </script>
  <link rel="stylesheet" href="/assets/styles.css?v=18">
  <script src="/assets/consent.js?v=1" defer></script>
</head>
<body>
'''


def article_page(a):
    url = f'{SITE}/insights/{a["slug"]}/'
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "@id": url + "#article", "headline": a['title'], "description": a['desc'],
         "url": url, "datePublished": a.get('date', PUBLISHED), "dateModified": DATE, "inLanguage": "en",
         "author": {"@id": f"{SITE}/#org"}, "publisher": {"@id": f"{SITE}/#org"},
         "mainEntityOfPage": url, "about": a['about'], "keywords": ", ".join(a['keywords'])},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "JustDukkan", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Insights", "item": SITE + "/insights/"},
            {"@type": "ListItem", "position": 3, "name": a['short'], "item": url}]},
        {"@type": "Organization", "@id": f"{SITE}/#org", "name": "JustDukkan", "legalName": "JustDukkan, LLC", "url": SITE + "/"},
    ]}
    if a.get('faq'):
        ld['@graph'].append({"@type": "FAQPage", "@id": url + "#faq", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": ans}} for q, ans in a['faq']]})
    faq_html = ''
    if a.get('faq'):
        faq_html = '<h2>Frequently asked questions</h2>\n' + ''.join(f'<h3>{q}</h3>\n<p>{ans}</p>\n' for q, ans in a['faq'])
    body = f'''{header('insights')}
  <main>
    <section class="article-hero">
      <div class="container">
        <nav class="breadcrumb" aria-label="Breadcrumb"><a href="/">JustDukkan</a><span>/</span><a href="/insights/">Insights</a><span>/</span><span>{a['short']}</span></nav>
        <h1 class="display" style="margin-top:28px">{a['title']}</h1>
        <p class="lede">{a['desc']}</p>
        <p class="article-meta">JustDukkan · {a['read']} min read · Updated {DATE}</p>
      </div>
    </section>
    <section class="article" style="border-top:0;padding-top:0">
      <div class="container">
        <div class="prose">
{a['body']}
{faq_html}
        </div>
        <div class="article-cta">
          <strong>Have a process like this?</strong>
          <p>We look at the process, design the agent team it needs, and decide together whether it is worth building. No packages, no price list.</p>
          <a href="mailto:enes@justdukkan.com?subject=Solution%20consultation" class="btn btn-primary">Get in touch <span class="arrow">→</span></a> <a href="/#contact" class="btn btn-ghost">Book a call</a>
        </div>
      </div>
    </section>
  </main>
{FOOTER}{CAL_SNIPPET}</body>
</html>
'''
    return head(a['title'] + ' — JustDukkan', a['desc'], url, ld) + body


def index_page():
    url = f'{SITE}/insights/'
    ld = {"@context": "https://schema.org", "@type": "CollectionPage", "@id": url, "url": url,
          "name": "Insights — JustDukkan", "inLanguage": "en",
          "description": "Practical notes on building custom AI agent teams: hub-and-spoke architecture, MCP servers and tools, agent skills, API integration and what it takes to keep a system running.",
          "hasPart": [{"@type": "Article", "headline": a['title'], "url": f'{SITE}/insights/{a["slug"]}/'} for a in ARTICLES]}
    cards = ''.join(f'''          <a class="insight-card" href="/insights/{a['slug']}/">
            <span class="label">{a['kicker']}</span>
            <h3>{a['title']}</h3>
            <p>{a['desc']}</p>
            <span class="more">Read →</span>
          </a>
''' for a in ARTICLES)
    body = f'''{header('insights')}
  <main>
    <section class="article-hero">
      <div class="container">
        <h1 class="display">Notes from the architecture desk.</h1>
        <p class="lede">How we design, build and maintain agent teams that hold up in production: patterns, checklists and the trade-offs behind them.</p>
      </div>
    </section>
    <section style="border-top:0;padding-top:0">
      <div class="container">
        <div class="insights-list">
{cards}        </div>
      </div>
    </section>
  </main>
{FOOTER}{CAL_SNIPPET}</body>
</html>
'''
    return head('Insights — JustDukkan', ld['description'], url, ld) + body


def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)
    print('wrote', os.path.relpath(path, ROOT))


write(os.path.join(ROOT, 'insights', 'index.html'), index_page())
for a in ARTICLES:
    write(os.path.join(ROOT, 'insights', a['slug'], 'index.html'), article_page(a))
