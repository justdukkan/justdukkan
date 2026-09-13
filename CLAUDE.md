# justdukkan.com — CLAUDE.md

Bu dosya, siteye sıfır bağlamla giren birinin ihtiyaç duyacağı her şeyi içerir. Önce bunu oku; ayrıntı için `tasks/todo.md` ve git geçmişi.

## 1. Ne bu?

**JustDukkan, LLC**'nin kurumsal sitesi. Konum: **AI solutions architecture** — süreç otomasyonu, sistem/çözüm mimarisi, agentic sistemler (hub-and-spoke orkestrasyon, MCP sunucuları, tipli tool'lar). Hedef: şirketlerin iç süreçlerini otomatikleştirip iş yapış şeklini ve maliyetini değiştirmek.

Kararlar (Enes, 2026-09-13):
- **Kurumsal** ton; kişisel bilgi/isim yok (Enes'in adı sadece e-posta adresinde).
- **Fiyat yok, paket yok**; talep gelince görüşülür.
- **Birincil CTA = e-posta** ("Get in touch" / "Bize yazın" → `mailto:enes@justdukkan.com?subject=Solution%20consultation`). Cal.com görüşme takvimi **ikincil**.
- Varsayılan dil **EN**, ikinci dil **TR** (`/tr/`). Otomatik dil yönlendirmesi yok.
- Sertifikalar (Claude Certified Architect – Foundations alınıyor; AWS SA ve Google Cloud AI Architect planlı) sitede **gösterilmiyor**; onların yerine "designed to work with the models your business already uses" model logoları bandı var.
- Uydurma metrik/rakam yazma; vaka çalışması gelene kadar sonuçlar nitel.
- **Google Analytics 4** yalnızca çerez banner'ında "Accept" sonrası yüklenir (Consent Mode değil; onay yokken Google'a hiç istek gitmez). Gizlilik sayfası `/privacy/` + `/tr/gizlilik/`.
- Site sıfırdan yeniden yazıldı 2026-09-13; eski "Digital Products & Creative Services" sayfasından hiçbir şey kalmadı.

## 2. Şirket bilgileri (sitede ve tüm dış profillerde birebir aynı)

- Yasal ad **JustDukkan, LLC** · marka **JustDukkan** · Delaware, USA · **EIN 38-4388070**
- Adres: **1111B S Governors Ave, Suite 46654, Dover, DE 19904, USA**
- E-posta **enes@justdukkan.com** · Tel/WhatsApp **+1 (910) 679-9657** (`tel:+19106799657`, `https://wa.me/19106799657`)
- Tagline: *AI solutions architecture: automation, system design and agentic systems.*
- Cal.com: **`cal.com/justdukkan/solution-consultation`** (event "Solution Consultation", profil adı "JustDukkan, LLC"/"JustDukkan AI", Google Meet, Europe/Istanbul). Eski `enes-ertas-5wscht/secret` linki ölü.
- LinkedIn: **linkedin.com/company/justdukkan-llc** (kapak: `brand/linkedin-cover.png`, avatar: `.j` favicon)
- GitHub org: **github.com/justdukkan** (Enes = owner; kişisel hesap `ertasenes`)
- PyPI: `invoice-intake-mcp` · MCP Registry: `com.justdukkan/invoice-intake-mcp`

## 3. Altyapı ve deploy

- Repo **`github.com/justdukkan/justdukkan`**, **public** (Vercel Hobby org'a ait private repoyu desteklemiyor), branch `main`. Lokal: `~/projects/justdukkan`.
- **Vercel** projesi `justdukkan` (team `enes-projects-d11e82d9`, id `prj_GkA9hqmjpvcXCZeSBcnWATODEAL6`), GitHub'a bağlı → **push = production deploy** (~1 dk). `vercel deploy` gerekmez. Vercel CLI `ertasenes` olarak giriş yapmış; `~/Library/Application Support/com.vercel.cli/auth.json` token'ı REST API için geçersiz (CLI çalışıyor).
- Vercel GitHub App org'da **sadece `justdukkan` reposuna** erişmeli. Yeni repo eklenirse Vercel otomatik proje açıp build hatası verir (invoice-intake-mcp'de oldu, proje silindi).
- Domain **justdukkan.com** + www. DNS **Cloudflare** (proxy açık; e-posta adreslerini obfuscate ediyor; CSS/JS'i cache'liyor → §7). HTTP→HTTPS 308 var; **www → apex yönlendirmesi YOK** (www ayrı 200 dönüyor; yapılacaklar §9).
- Build/framework yok: düz statik HTML + CSS + biraz JS.
- Cloudflare DNS'te ayrıca: Search Console TXT, **MCP Registry TXT** (`v=MCPv1; k=ed25519; p=tHH6Ral+Br4oXDYJjId2KfdlL4GnJtUgHXrgnwy4Ums=`, apex).

## 4. Dosya envanteri

```
index.html                    EN ana sayfa (default). Inline: tema script'i (head), Cal.com embed (body sonu), JSON-LD
tr/index.html                 TR ana sayfa — aynı markup, çevrilmiş metin, hreflang çapraz bağlı
insights/index.html           Makale listesi (EN)              } ÜRETİLİR — elle düzenleme,
insights/<slug>/index.html    Makaleler (EN)                   } tools/build_insights.py çalıştır
tools/articles.py             Makale içerikleri (KAYNAK). Python list of dicts: slug, short, kicker, title, desc, read, about, keywords, body(HTML), faq
tools/build_insights.py       Üretici: head/header/footer/JSON-LD (Article+Breadcrumb+FAQPage)/theme script/Cal snippet. THEME_JS ve CAL_SNIPPET sabitleri; styles.css?v= burada da güncellenir
assets/styles.css             Tüm CSS: tokenlar, light/dark, header, hero, models, cards, expertise, demo, outcomes, steps, FAQ, contact, footer, articles, responsive
assets/demo.js                İnteraktif "orchestrator" demosu (§5)
assets/consent.js             Çerez banner'ı + GA4 yükleyici. Başta GA_ID; localStorage["jd-consent"]=granted|denied; banner DOM'u JS'te (EN/TR lang'a göre); window.jdConsent.open() tercihi sıfırlayıp banner'ı yeniden açar
privacy/index.html            Gizlilik ve çerez sayfası (EN); "Change cookie choice" butonu jdConsent.open()
tr/gizlilik/index.html        Aynısı TR. İkisi de elle yazılmış (header/footer index.html / tr/index.html'den); metin değişince ikisini de güncelle
assets/wordmark.png           ".justdukkan" logosu — beyaz harfler + alfa; CSS `mask` + currentColor ile tema rengini alır
assets/favicon.svg/-32.png/-512.png, apple-touch-icon.png   ".j" glifi (wordmark'tan kırpıldı), koyu yuvarlak kare
brand/linkedin-cover.png (2256×382), linkedin-cover-1x.png  LinkedIn kapak: koyu zemin, sağda ".j"
llms.txt                      LLM crawler'ları için şirket/hizmet/makale/iletişim özeti (markdown)
robots.txt                    Herkese Allow; AI crawler'lar (GPTBot, ClaudeBot, PerplexityBot, Google-Extended…) açıkça Allow; Sitemap satırı
sitemap.xml                   /, /tr/ (hreflang), /insights/ + 4 makale
9ab21623bd51863e0413867377354055.txt   IndexNow anahtar dosyası (§8)
README.md                     Kısa repo açıklaması
tasks/todo.md                 İş listesi (geçmiş fazlar işaretli)
```

## 5. Sayfa yapısı (ana sayfa, EN/TR aynı sıra)

1. **Header** (sticky 52px): wordmark · Services · Expertise · Approach · Insights · Contact · **tema toggle** (ay/güneş) · EN/TR · **"Get in touch →"** (mailto)
2. **Hero**: "We design the AI architecture behind how your company works." + alt metin + "Get in touch" (mailto) + "What we do" (`#services`)
3. **Models bandı**: Claude, ChatGPT, Gemini, Kimi, DeepSeek, Mistral, Llama, Qwen, Grok — monokrom inline SVG (lobehub `@lobehub/icons-static-svg`), tek satır
4. **Services** (3 kart): Process Automation · System & Solution Architecture · Agentic Systems
5. **Expertise** (8 madde, 2 sütun): hub-and-spoke, MCP & tool design, multi-agent workflows, knowledge/retrieval, evals & guardrails, cloud (AWS/GCP), integration, cost & operations
6. **Reference pattern → interaktif demo** (`#demo`, `assets/demo.js`): mock "JustDukkan Orchestrator" konsolu. Sol: 3 çalıştırma (Invoice intake / Support triage / Vendor onboarding). Orta: animasyonlu log (orchestrator → agent → tool çağrısı → **Human review: Approve/Reject** → done). Sağ: spoke'lar (aktif olan yeşil), tool sayacı, Replay. Sabit yükseklik 460px, log içeride kayar. Görünür olunca otomatik başlar (scroll-rect kontrolü; IntersectionObserver arka plan sekmesinde çalışmadığı için kullanılmadı). EN/TR string'ler `document.documentElement.lang`'a göre.
7. **Outcomes** (3): manual hours → automated flows · cost per process → lower unit cost · days → faster cycle time
8. **Approach** (4 adım): 01 · Discover → 02 · Architect → 03 · Build → 04 · Operate
9. **FAQ** (7 soru, `<details>` akordeon, ilki açık; FAQPage schema)
10. **Contact** (`#contact`): başlık + açıklama → **"Get in touch" butonu** (mailto) + "Tell us about the process in a few lines and we will get back to you as soon as possible." → ayraç **"or book a call"** → **Cal.com inline embed** (`#cal-inline`)
11. **Footer**: wordmark + EN/TR; sütunlar Company (yasal ad, adres, EIN) / Contact (e-posta, tel, WhatsApp) / Insights (4 makale); "© 2026 JustDukkan, LLC"

**Insights** (`/insights/`, EN): liste + 4 makale — hub-and-spoke-agent-architecture, mcp-server-and-tool-design, process-automation-architecture, human-in-the-loop-for-agentic-systems. Her makale: breadcrumb, hero, prose (720px), makale sonu FAQ, CTA kutusu ("Get in touch" mailto + "Book a call" `/#contact`). TR makale yok; TR sayfasındaki Insights linki EN'e gider.

Bölüm başlıklarının üstünde küçük "eyebrow" etiket **yok** (kaldırıldı; sadece models bandında bir etiket var). Metinlerde uzun çizgi (—) **kullanılmıyor**.

## 6. Tasarım sistemi

- Referans: **cursor.com**'un yapısal dili (renk, tipografi, container'lar); içerik değil.
- Tokenlar (`:root`): bg `#f7f7f4` · fg `#26251e` · card `#f0efeb` · card-hover `#ebeae5` · accent `#34785c`. Dark: bg `#14120b` · fg `#edecec` · card `#1b1913` · hover `#201e18` · accent `#4fa37e`.
- **Tema**: varsayılan sistem tercihi. Toggle `data-theme="light|dark"` yazar, `localStorage["jd-theme"]`'de saklar. Head'deki inline `jdTheme` script'i (`current()`, `toggle()`) flash'ı önler. **Dark tokenlar CSS'te iki yerde**: `@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) }` ve `:root[data-theme="dark"]` — token eklerken ikisini de güncelle. Toggle ikonu da aynı iki seçiciyle değişir.
- **Tek font: Inter** (Google Fonts, 400/500/600). Başlıklar Inter 400, `letter-spacing -0.03em`. Serif/JetBrains Mono YOK; kod için sistem mono.
- Container akışkan: `padding: 0 clamp(20px, 9vw, 180px)`, `max-width 1800px`. Prose 680–720px. Demo, takvim, FAQ ~820–1040px.
- Butonlar: primary (fg zemin, bg yazı, hover accent) + ghost (1px border). Kartlar 1px border, radius 12px, gölge yok.
- Logo: yalnızca wordmark; ekstra işaret/ikon ekleme.
- Cal.com: inline embed (`Cal.ns.consultation("inline", …)`), tema `jdTheme.current()`; toggle'da embed **yeniden oluşturulur** (Cal'ın `ui` tema güncellemesi inline'da işlemiyor). Renkler `cssVarsPerTheme` ile site paletine eşlenmiş. Alt "Cal.com" yazısı iframe'in alt 90px'i kırpılarak gizleniyor (`.cal-inline iframe { margin-bottom:-90px; clip-path: inset(0 0 90px 0) }`; `clip-path` şart, çünkü form adımında iframe 530px'e düşüyor ve `.cal-inline`'ın `min-height:560px`'i yalnız negatif margin ile kırpmayı boşa çıkarıyordu); `hideEventTypeDetails:false` (sol panelde "JustDukkan · Solution Consultation" görünür).
- Responsive: ≤900px grid'ler 2 sütun, demo sağ panel gizli; ≤640px tek sütun, nav linkleri gizli, demo yüksekliği auto. Yatay taşma olmamalı.

## 7. Cache-bust kuralı (ÖNEMLİ)

Cloudflare `styles.css`, `demo.js` ve `consent.js`'i cache'ler. Bunlar değişince **`?v=N`'i artır**: `index.html`, `tr/index.html`, `tools/build_insights.py` (sonra build), **`privacy/index.html`, `tr/gizlilik/index.html`**. Şu an **styles.css?v=16**, **demo.js?v=8**, **consent.js?v=1**. Artırmazsan canlıda eski CSS + yeni HTML görünür ("site bozuldu" olayının sebebi buydu). HTML cache'lenmez; canlı kontrolde yine de `?x=<rastgele>` ekle. Favicon linkleri `?v=2`.

## 8. SEO / GEO — yapılanlar

- **JSON-LD `@graph`** (ana sayfalar): `Organization`+`ProfessionalService` (yasal ad, adres, EIN=`taxID`, telefon, e-posta, diller, `knowsAbout`, 3 hizmetlik `OfferCatalog`, `contactPoint`→Cal, `sameAs`: LinkedIn, GitHub org, Cal), `WebSite`, `WebPage`, `FAQPage`. Makalelerde `Article` + `BreadcrumbList` + `FAQPage`. Değişiklikte JSON geçerliliğini kontrol et.
- **GA4**: Measurement ID `consent.js` başında (`GA_ID`). Property Enes'in Google hesabında. Onay modeli §1.
- `llms.txt`, `robots.txt`, `sitemap.xml` (/, /tr/, insights ×5, /privacy/, /tr/gizlilik/), `<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">`, canonical, hreflang en/tr/x-default, OG meta, theme-color.
- **Google Search Console**: domain property doğrulandı (DNS TXT), sitemap gönderildi (2026-09-13). Insights sayfaları indekslendi; `/` beklemede (eski içerikli URL yeniden değerlendiriliyor; www dublikasyonu olası neden).
- **Bing Webmaster**: GSC'den import edildi (sitemap 48 saat sonra görünür dendi).
- **IndexNow**: anahtar `9ab21623bd51863e0413867377354055` (dosya repoda). 7 URL gönderildi (202). Yeni/değişen sayfa için:
  `curl -X POST https://api.indexnow.org/indexnow -H 'Content-Type: application/json' -d '{"host":"justdukkan.com","key":"9ab21623bd51863e0413867377354055","keyLocation":"https://justdukkan.com/9ab21623bd51863e0413867377354055.txt","urlList":["https://justdukkan.com/…"]}'`
- **Dış varlıklar**: LinkedIn şirket sayfası (About metni = llms.txt özeti); GitHub org; **`github.com/justdukkan/invoice-intake-mcp`** (MIT, Python, mcp 2.x `MCPServer`; read/commit iki server, tipli hatalar, sunucu tarafı onay kilidi, audit log, orkestratör, pytest + evals; lokal `~/projects/invoice-intake-mcp`, venv Python 3.12) → PyPI `invoice-intake-mcp` 0.1.1 (`uvx invoice-intake-mcp --role read|commit`) → **MCP Registry `com.justdukkan/invoice-intake-mcp` v0.1.1 active** (DNS auth; özel anahtar `~/.config/mcp-registry/justdukkan-ed25519.pem`, repoya girmez). GitHub org namespace'i (`io.github.justdukkan`) çalışmadı (OAuth app org rolünü görmedi) — DNS yolu kullan.
- **awesome-mcp-servers PR #14311** açık (fork `justdukkan/awesome-mcp-servers`, branch `add-invoice-intake-mcp`, Finance & Fintech bölümü).
- Cal.com profili: bio metni eklendi, isim JustDukkan, avatar wordmark.

## 9. SEO / GEO — yapılacaklar

- [ ] **www → apex 308** (Vercel → Project → Settings → Domains → www.justdukkan.com → Redirect to justdukkan.com). API token'ım geçersiz; Enes dashboard'dan yapacak.
- [ ] 48 saat sonra Search Console: `/` indekslendi mi, hata var mı; gerekirse URL Inspection → Request indexing.
- [ ] Bing Webmaster: sitemap ve IndexNow sekmesi; URL Submission ile makaleler.
- [ ] Clutch.co, GoodFirms, Crunchbase profilleri (Enes; §2 bilgileri + LinkedIn About metni; hizmet ağırlığı AI Consulting 40 / BPA 30 / Architecture 30).
- [ ] LinkedIn kişisel profil → JustDukkan "Founder, AI Solutions Architect" deneyimi; makaleleri LinkedIn'de paylaş.
- [ ] awesome-mcp-servers PR merge takibi.
- [ ] Ayda 1–2 Insights makalesi (aday: support triage mimarisi, AI otomasyon maliyet modeli, TR "şirketler için agentic sistemler 101"); TR çeviriler.
- [ ] İlk gerçek işten **vaka çalışması** — en güçlü sinyal.
- [ ] Sertifikalar alındıkça siteye/LinkedIn'e rozet (Enes onayıyla).
- [ ] Haftalık görünürlük testi: ChatGPT/Perplexity'de "AI solutions architecture consultancy", "MCP tool design consultant" vb.

## 10. Rutin işlemler

- **Metin/HTML değişikliği**: `index.html` + `tr/index.html` **ikisini de** güncelle → commit → push → 1 dk sonra `curl -sL "https://justdukkan.com/?x=$RANDOM" | grep …` ile doğrula.
- **CSS/JS değişikliği**: düzenle → `?v=N` artır (index, tr/index, build_insights, privacy ×2) → build_insights → commit/push.
- **Yeni makale**: `tools/articles.py`'a dict ekle → `python3 tools/build_insights.py` → `sitemap.xml` + `llms.txt` + ana sayfa footer "Insights" listesi (EN ve TR) → IndexNow ping.
- **Hizmet/şirket bilgisi değişikliği**: HTML + JSON-LD + `llms.txt` + LinkedIn/dış profiller senkron.
- **invoice-intake-mcp yeni sürüm**: `pyproject.toml` + `server.json` version → `.venv/bin/python -m build` → Enes: `.venv/bin/twine upload dist/*` (`__token__` + PyPI token) → `mcp-publisher login dns --domain justdukkan.com --private-key "$(/opt/homebrew/opt/openssl@3/bin/openssl pkey -in ~/.config/mcp-registry/justdukkan-ed25519.pem -noout -text | grep -A3 priv: | tail -n +2 | tr -d ' :\n')" && mcp-publisher publish`.
- **Lokal önizleme**: `python3 -m http.server 8765 --bind 127.0.0.1` (repo kökünde); Chrome MCP ile macmini tarayıcısı. Arka plan sekmesinde timer/IO throttling olur; demo testini görünür sekmede yap.
- **Terminal notu (Enes)**: Claude Code prompt'unda `! komut` çalıştırılır; zsh'de `!` yazma.

## 11. Bilinen tuhaflıklar

- Vercel CLI `vercel ls` çıktısı bazen boş görünür; deploy'u `https://justdukkan.com` içeriğinden doğrula.
- Cloudflare e-posta adreslerini `/cdn-cgi/l/email-protection` ile değiştirir; canlı HTML'de `enes@` aramak başarısız olabilir.
- Cal.com embed dar ekranda (<~768px) mobil düzene geçer (takvim tek sütun).
- ≤~410px genişlikte header'daki CTA butonu yüzünden hafif yatay taşma var (banner'dan önce de vardı).
- Search Console'da property "Domain" tipi olduğu için Bing import'unda "https://" boş görünmüştü; normal.
- Cal.com embed'i, Enes'in cal.com'a giriş yaptığı tarayıcıda formu hesap bilgileriyle (ad/e-posta) dolu ve hesap dilinde (TR) gösterir; ziyaretçi bunları görmez. Dil ziyaretçinin `Accept-Language`'ına göre gelir, embed'de dil zorlayan parametre yok (`lang/locale/hl/lng`, `NEXT_LOCALE` denendi, işlemiyor). Kontrol için gizli pencere kullan.
