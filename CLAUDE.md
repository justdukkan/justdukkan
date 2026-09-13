# justdukkan.com — CLAUDE.md

Kurumsal site: **JustDukkan, LLC** — AI solutions architecture (süreç otomasyonu, sistem tasarımı, agentic sistemler). Kişisel bilgi yok, fiyat yok. Varsayılan dil EN, ikinci dil TR. Sıfırdan yeniden yazıldı: 2026-09-13.

## Şirket bilgileri (sitede ve tüm dış profillerde birebir aynı kullan)

- Yasal ad: **JustDukkan, LLC** · Marka: **JustDukkan** · Delaware, USA · EIN 38-4388070
- Adres: 1111B S Governors Ave, Suite 46654, Dover, DE 19904, USA
- E-posta: enes@justdukkan.com · Tel/WhatsApp: +1 (910) 679-9657 (`wa.me/19106799657`)
- Tagline: *AI solutions architecture: automation, system design and agentic systems.*
- Cal.com: `cal.com/justdukkan/solution-consultation` (event "Solution Consultation", profil adı "JustDukkan, LLC")
- LinkedIn: linkedin.com/company/justdukkan-llc · GitHub org: github.com/justdukkan
- Sertifikalar: Claude Certified Architect – Foundations (alınıyor), AWS SA ve Google Cloud AI Architect (planlı). Sitede sertifika bandı YOK; model logoları var.

## Altyapı

- Repo: `github.com/justdukkan/justdukkan` (**public**; Vercel Hobby, org'a ait private repoyu desteklemiyor) · branch `main`
- Deploy: Vercel projesi `justdukkan` (team `enes-projects-d11e82d9`), GitHub'a bağlı → **push = production deploy**. `vercel deploy` gerekmez.
- Domain: justdukkan.com + www; DNS **Cloudflare** (proxy açık; e-posta obfuscation yapıyor).
- Vercel GitHub App org'da sadece `justdukkan` reposuna erişmeli; yeni repo eklenirse Vercel proje açmaya çalışır (invoice-intake-mcp için oldu, silindi).
- Build yok, statik HTML. Framework yok.

## Dosya yapısı

```
index.html                 EN ana sayfa (default)
tr/index.html              TR ana sayfa — aynı markup, çevrilmiş metin; hreflang çapraz bağlı
insights/index.html        Makale listesi (EN)
insights/<slug>/index.html Makaleler — ÜRETİLİR, elle düzenleme
tools/articles.py          Makale içerikleri (kaynak). Düzenle → python3 tools/build_insights.py
tools/build_insights.py    Makale sayfası üretici (header/footer/JSON-LD/breadcrumb)
assets/styles.css          Tüm CSS (design tokens, light/dark, bileşenler, responsive)
assets/demo.js             İnteraktif orkestratör demosu (3 senaryo, Approve/Reject, EN+TR string'ler)
assets/wordmark.png        ".justdukkan" logosu (alfa maske; CSS mask + currentColor ile renklenir)
assets/favicon*.png/svg    ".j" glifi favicon seti, apple-touch-icon
brand/linkedin-cover.png   LinkedIn kapak (2256×382)
llms.txt                   LLM crawler'ları için şirket/hizmet özeti
robots.txt                 AI crawler'lara açık Allow + sitemap
sitemap.xml                EN/TR hreflang + insights sayfaları
tasks/todo.md              İş listesi
```

## Tasarım kuralları

- cursor.com'un yapısal dili: bg `#f7f7f4` / dark `#14120b`, fg `#26251e` / `#edecec`, card `#f0efeb` / `#1b1913`, accent `#34785c` / `#4fa37e`. Light varsayılan, `prefers-color-scheme` ile dark.
- **Tek font: Inter** (Google Fonts). Serif yok, JetBrains Mono yok. Kod için sistem mono stack.
- Container akışkan: `padding: 0 clamp(20px, 9vw, 180px)`, max 1800px. Metin blokları 680–720px. Demo ve takvim 1040px.
- Bölüm başlıklarının üstünde küçük "eyebrow" etiket YOK (kaldırıldı). Metinlerde uzun çizgi (—) kullanma; virgül/noktalı virgül.
- Header: wordmark solda, linkler (Services, Expertise, Approach, Insights, Contact), **tema toggle** (ay/güneş), EN/TR, "Book a call" → `#contact`.
- Tema: varsayılan sistem tercihi; toggle `data-theme="light|dark"` yazar, `localStorage['jd-theme']`'de tutar. Head'deki inline `jdTheme` script'i flash'ı önler (her HTML'de + build_insights.py `THEME_JS`). CSS'te dark tokenlar iki yerde: `@media (prefers-color-scheme: dark) :root:not([data-theme="light"])` ve `:root[data-theme="dark"]` — token eklerken ikisini de güncelle. Cal.com teması `jdTheme.current()` ile senkron.
- Logo: sadece wordmark görseli; ekstra işaret/ikon ekleme.
- Cal.com iletişim bölümünde **inline embed** (`#cal-inline`), popup değil; renkler `cssVarsPerTheme` ile siteye eşlenmiş.

## Cache-bust kuralı (ÖNEMLİ)

Cloudflare `styles.css` ve `demo.js`'i cache'ler. CSS/JS değişince **her HTML'de** `?v=N` sürümünü artır (`index.html`, `tr/index.html`, `insights/**/index.html`; build_insights.py içindeki `styles.css?v=` de). Şu an **v=12**. Artırmazsan canlıda eski CSS + yeni HTML görünür ("site bozuldu" şikayetinin sebebi buydu).

## Sayfa bölümleri (ana sayfa, EN/TR)

Hero → Model logoları bandı (Claude, ChatGPT, Gemini, Kimi, DeepSeek, Mistral, Llama, Qwen, Grok — monokrom, lobehub icons) → Services (3 kart) → Expertise (8 madde) → Reference pattern: interaktif demo (sabit 460px) → Outcomes (3) → Approach (4 adım) → FAQ (7 soru, `<details>`) → Contact (Cal.com inline) → Footer (Company / Contact / Insights sütunları).

## SEO / GEO — yapılanlar

- JSON-LD `@graph`: Organization+ProfessionalService (adres, EIN, telefon, `knowsAbout`, 3 hizmetlik OfferCatalog, `sameAs`: LinkedIn, GitHub, Cal), WebSite, WebPage, FAQPage. Makalelerde Article + BreadcrumbList + FAQPage.
- `llms.txt`, `robots.txt` (GPTBot, ClaudeBot, PerplexityBot, Google-Extended vb. Allow), `sitemap.xml`, `<meta name="robots" content="index, follow, max-snippet:-1">`, canonical + hreflang (en/tr/x-default), OG meta.
- 4 EN makale (`/insights/`): hub-and-spoke, MCP tool design, process automation playbook, human-in-the-loop. TR makale yok.
- Google Search Console: domain property doğrulandı, sitemap gönderildi (2026-09-13); insights sayfaları indekslendi, `/` bekliyor. Bing Webmaster: GSC'den import edildi.
- **IndexNow** kuruldu: anahtar dosyası `/9ab21623bd51863e0413867377354055.txt` (repoda). Yeni/değişen URL'leri anında Bing'e bildirmek için:
  `curl -X POST https://api.indexnow.org/indexnow -H 'Content-Type: application/json' -d '{"host":"justdukkan.com","key":"9ab21623bd51863e0413867377354055","keyLocation":"https://justdukkan.com/9ab21623bd51863e0413867377354055.txt","urlList":["https://justdukkan.com/…"]}'` (202 = kabul).
- Dış varlıklar: LinkedIn şirket sayfası (kapak `brand/linkedin-cover.png`), GitHub org, açık kaynak referans repo **`github.com/justdukkan/invoice-intake-mcp`** — PyPI'da (`uvx invoice-intake-mcp`) ve **MCP Registry'de `com.justdukkan/invoice-intake-mcp`** (DNS auth: apex TXT `v=MCPv1; k=ed25519; p=…`, özel anahtar `~/.config/mcp-registry/justdukkan-ed25519.pem`). awesome-mcp-servers PR #14311 açık.

## SEO / GEO — yapılacaklar

- [ ] **www → apex 308 yönlendirmesi** (Vercel → Project → Settings → Domains → www.justdukkan.com → Redirect to justdukkan.com). Şu an www ayrı 200 dönüyor; canonical apex'i gösterse de Google eski www/eski içerik yüzünden `/`'i geç indeksliyor olabilir.
- [ ] 48 saat sonra Search Console: indekslenen sayfalar, hatalar; URL Inspection ile makaleleri "request indexing".
- [ ] Bing Webmaster: sitemap görünüyor mu, URL Submission ile makaleler.
- [ ] Clutch.co, GoodFirms, Crunchbase profilleri (Enes; metinler LinkedIn About ile aynı).
- [ ] LinkedIn kişisel profil → JustDukkan deneyimi (sayfa "1 çalışan" olsun); her makaleyi LinkedIn'de paylaş.
- [ ] awesome-mcp-servers PR merge takibi.
- [ ] Ayda 1–2 yeni Insights makalesi (aday: support triage mimarisi, AI otomasyon maliyet modeli, TR: "şirketler için agentic sistemler 101"). TR makale çevirileri.
- [ ] İlk gerçek işten **vaka çalışması** (süreç, mimari, önce/sonra) — LLM'lerin önerme kararında en güçlü sinyal.
- [ ] Sertifikalar geldikçe siteye/LinkedIn'e rozet.
- [ ] Haftalık: ChatGPT/Perplexity'de "AI solutions architecture consultancy Delaware" tarzı sorgularla görünürlük testi.
- [ ] `invoice-intake-mcp` yeni sürüm akışı: pyproject+server.json bump → build → `twine upload` (Enes token) → `mcp-publisher login dns --domain justdukkan.com --private-key … && mcp-publisher publish`.

## Çalışma kuralları

- Değişiklik = lokal düzenle → commit → push. Canlıyı `curl`/tarayıcıyla doğrula (Cloudflare için `?x=<rastgele>` ekle).
- İçerik değişince **iki dili de** güncelle (index.html + tr/index.html); makale/hizmet değişince llms.txt ve JSON-LD'yi de.
- Yeni makale: `tools/articles.py`'a ekle → build → `sitemap.xml`, `llms.txt`, ana sayfa footer "Insights" listesi.
- Uydurma metrik/rakam yazma (vaka çalışması gelene kadar nitel sonuçlar).
- Üçüncü parti logoları sadece model bandında, monokrom.
