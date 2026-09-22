# justdukkan.com — iş kaydı

**Açık işler burada değil, `CLAUDE.md` §9'da.** Bu dosya tamamlanmış fazların kaydını tutar; yeni faz bitince en üste bir blok ekle.

---

## 2026-09-22 — Pivot: şirkete özel AI agent takımları
Konum değişikliği: "AI solutions architecture" (3 hizmet) → hiyerarşik AI agent takımları kurmak ve bakımını yapmak (4 hizmet).

- [x] Ana sayfalar EN+TR: yeni hero, 4 hizmet kartı (Agent Team Design / Build & Deployment / Integrations: API & MCP / Operate & Maintain), expertise, outcomes, approach
- [x] FAQ 7 → 8 madde; yeni maddeler "hazır agent satmıyoruz" ve "bakım neleri kapsıyor"
- [x] JSON-LD: org description, knowsAbout, OfferCatalog (4 offer), FAQPage (8 Q/A), WebPage adı
- [x] llms.txt, README, insights index metni; demo.js etiketleri "agent team" (v9)
- [x] 6 yeni EN makale: designing-the-agent-team, agent-topologies, connecting-agents-to-your-apis, agent-skills, delegate-to-human, operating-agentic-systems
- [x] Mevcut 4 makalede kicker + sıra; footer ilk 4 makale + "All insights"; `date` alanı ile datePublished/dateModified ayrıldı
- [x] sitemap 15 URL, IndexNow ping (9 URL)
- [x] Layout: içerik sütunu `--container` 1800 → 1360 → 1400px (styles v19, v20)
- [x] CLAUDE.md yeniden yapılandırıldı (§0 durum özeti, §9 tek açık iş listesi)

## 2026-09-13 (gece) — Analytics ve gizlilik
- [x] GA4 `G-C8T8T596HD` + çerez onay banner'ı (`assets/consent.js`, yalnız "Accept" sonrası yüklenir)
- [x] `/privacy/` ve `/tr/gizlilik/` sayfaları, footer linkleri, sitemap
- [x] Cal.com branding form adımında da gizlendi (clip-path)
- [x] www → apex yönlendirmesi devrede (Vercel, 307)

## 2026-09-13 (akşam) — Görünürlük ve açık kaynak
- [x] Tema toggle (persist, flash yok, Cal.com ile senkron)
- [x] Contact: e-posta birincil, Cal.com ikincil ("or book a call")
- [x] IndexNow kuruldu, 7 URL gönderildi
- [x] invoice-intake-mcp: PyPI 0.1.1 + MCP Registry `com.justdukkan` (DNS auth); awesome-mcp-servers PR #14311 açıldı
- [x] 4. makale (human-in-the-loop), LinkedIn kapak görseli

## 2026-09-13 — AI görünürlüğü fazı 2
- [x] FAQ bölümü (EN+TR) + FAQPage JSON-LD
- [x] `/insights/` index + ilk makaleler; `tools/build_insights.py` + `tools/articles.py` üretim hattı
- [x] Nav/footer Insights linkleri, sitemap + llms.txt

## 2026-09-13 — Sıfırdan yeniden yazım
Eski "Digital Products & Creative Services" sitesinden hiçbir şey kalmadı.

- [x] `assets/styles.css`: tokenlar, light/dark, bileşenler, responsive
- [x] `index.html` (EN) ve `tr/index.html` (TR) + hreflang
- [x] Favicon, OG meta, Cal.com event linki
- [x] Lokal doğrulama (light/dark, yatay taşma, anchor'lar) → deploy → canlı doğrulama

### Not
- Fontlar başlangıçta Inter + EB Garamond + JetBrains Mono idi; sonra **tek font Inter**'e indirildi (CLAUDE.md §6).
