# justdukkan.com — CLAUDE.md

Bu dosya, siteye sıfır bağlamla giren birinin ihtiyaç duyacağı her şeyi içerir. Önce §0'ı oku, sonra ilgili bölüme git. Açık işler §9'da, geçmiş `tasks/todo.md` ve git log'unda.

## 0. Şu an ne durumda? (son güncelleme 2026-09-23)

| | |
|---|---|
| **Site** | https://justdukkan.com canlı, Vercel'de, `main`'e her push production deploy (~1 dk) |
| **Konum** | Şirkete özel hiyerarşik AI agent takımları kurmak ve bakımını yapmak (2026-09-22 pivotu, §1) |
| **Sayfalar** | EN `/` · TR `/tr/` · `/about/` + `/tr/hakkinda/` · `/work/` (EN) · `/insights/` + **10 makale (EN)** · `/privacy/` + `/tr/gizlilik/` |
| **Teknoloji** | Build yok. Düz HTML + tek CSS + 2 küçük JS. Tek üretici script: `tools/build_insights.py` |
| **Canlı sürümler** | `styles.css?v=21` · `demo.js?v=9` · `consent.js?v=1` (değiştirince artır, §7) |
| **Analytics** | GA4 `G-C8T8T596HD`, yalnız çerez onayından sonra yüklenir |
| **Son commit'ler** | SEO/AI görünürlük turu: header taşması düzeldi, OG görselleri, `vercel.json`, `/about/` + `/work/`, `llms-full.txt` |
| **Bilinen açık hata** | Yok. Header taşması 2026-09-23'te düzeltildi (320-1440px ölçüldü). |
| **Sırada ne var** | §9. Kısaca: Enes'te dashboard ve dış profil işleri (GSC/GA/LinkedIn/dizinler), kodda TR makale kararı, içerikte ilk gerçek vaka çalışması. |

**İlk 5 dakikada bilmen gerekenler:** metin değişiyorsa EN **ve** TR ikisini birden güncelle · FAQ metni her sayfada iki yerde duruyor (JSON-LD + görünür blok) · CSS/JS değişince `?v=N` artırmazsan canlı bozuk görünür · `insights/` altındaki HTML'ler üretilir, elle düzenleme.

## 1. Ne bu?

**JustDukkan, LLC**'nin kurumsal sitesi. Konum (2026-09-22 pivotu): **şirkete özel hiyerarşik AI agent takımları kurmak ve bakımını yapmak**. Orkestratör + uzman agent'lar (hub-and-spoke), size özel yazılan tool'lar ve skill'ler, API entegrasyonları, MCP sunucuları, sonra düzenli bakım. **Hazır/abonelik agent satmıyoruz**; her sistem müşteriye özel kurulur ve müşteriye aittir.

Kararlar (Enes, 2026-09-13 / pivot 2026-09-22):
- **Kurumsal** ton; kişisel bilgi/isim yok (Enes'in adı sadece e-posta adresinde).
- **Fiyat yok, paket yok**; talep gelince görüşülür.
- **Birincil CTA = e-posta** ("Get in touch" / "Bize yazın" → `mailto:enes@justdukkan.com?subject=Solution%20consultation`). Cal.com görüşme takvimi **ikincil**.
- Varsayılan dil **EN**, ikinci dil **TR** (`/tr/`). Otomatik dil yönlendirmesi yok.
- Sertifikalar (Claude Certified Architect – Foundations alınıyor; AWS SA ve Google Cloud AI Architect planlı) sitede **gösterilmiyor**; onların yerine "designed to work with the models your business already uses" model logoları bandı var.
- Uydurma metrik/rakam yazma; vaka çalışması gelene kadar sonuçlar nitel.
- **4 hizmet** (ana sayfada 4 kart, JSON-LD OfferCatalog'da 4 offer): Agent Team Design · Build & Deployment · Integrations: API & MCP · Operate & Maintain. Approach adımları bunlarla birebir hizalı.
- "Hazır agent satmıyoruz" ayrımı iki yerde geçer: hero lede son cümlesi ve FAQ'nun 2. maddesi. Rakip ismi verilmez.
- **Google Analytics 4** yalnızca çerez banner'ında "Accept" sonrası yüklenir (Consent Mode değil; onay yokken Google'a hiç istek gitmez). Gizlilik sayfası `/privacy/` + `/tr/gizlilik/`.
- Site sıfırdan yeniden yazıldı 2026-09-13; eski "Digital Products & Creative Services" sayfasından hiçbir şey kalmadı.

## 2. Şirket bilgileri (sitede ve tüm dış profillerde birebir aynı)

- Yasal ad **JustDukkan, LLC** · marka **JustDukkan** · Delaware, USA · **EIN 38-4388070**
- Adres: **1111B S Governors Ave, Suite 46654, Dover, DE 19904, USA**
- E-posta **enes@justdukkan.com** · Tel/WhatsApp **+1 (910) 679-9657** (`tel:+19106799657`, `https://wa.me/19106799657`)
- Tagline: *Custom agentic systems: hierarchical AI agent teams built for your company.*
- Cal.com: **`cal.com/justdukkan/solution-consultation`** (event "Solution Consultation", profil adı "JustDukkan, LLC"/"JustDukkan AI", Google Meet, Europe/Istanbul). Eski `enes-ertas-5wscht/secret` linki ölü.
- LinkedIn: **linkedin.com/company/justdukkan-llc** (kapak: `brand/linkedin-cover.png`, avatar: `.j` favicon)
- GitHub org: **github.com/justdukkan** (Enes = owner; kişisel hesap `ertasenes`)
- PyPI: `invoice-intake-mcp` · MCP Registry: `com.justdukkan/invoice-intake-mcp`

## 3. Altyapı ve deploy

- Repo **`github.com/justdukkan/justdukkan`**, **public** (Vercel Hobby org'a ait private repoyu desteklemiyor), branch `main`. Lokal: `~/projects/justdukkan`.
- **Vercel** projesi `justdukkan` (team `enes-projects-d11e82d9`, id `prj_GkA9hqmjpvcXCZeSBcnWATODEAL6`), GitHub'a bağlı → **push = production deploy** (~1 dk). `vercel deploy` gerekmez. Vercel CLI `ertasenes` olarak giriş yapmış; `~/Library/Application Support/com.vercel.cli/auth.json` token'ı REST API için geçersiz (CLI çalışıyor).
- Vercel GitHub App org'da **sadece `justdukkan` reposuna** erişmeli. Yeni repo eklenirse Vercel otomatik proje açıp build hatası verir (invoice-intake-mcp'de oldu, proje silindi).
- Domain **justdukkan.com** + www. DNS **Cloudflare** (proxy açık; e-posta adreslerini obfuscate ediyor; CSS/JS'i cache'liyor → §7). HTTP→HTTPS 308 var; **www → apex 307** Vercel Domains'te tanımlı (2026-09-13; www DNS-only CNAME → vercel-dns, apex Cloudflare proxy'li → Vercel "Proxy Detected" uyarısı normal). 308'e çevirmek ve apex'i DNS-only yapmak opsiyonel.
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
about/index.html              Hakkında (EN); tr/hakkinda/index.html TR eşi. Elle yazıldı, kurucu adı YOK (§1 kurumsal ton kararı)
work/index.html               Açık kaynak vaka çalışması: invoice-intake-mcp (EN). Metrik ve müşteri adı yok
assets/og-cover.png, og-cover-tr.png   1200×630 paylaşım görselleri. Kaynak: brand/og-source.html + brand/fonts/ (Inter woff2, gömülü)
brand/og-source.html          OG kartlarının kaynağı; yeniden üretmek için §10'daki headless Chrome komutu
llms-full.txt                 ÜRETİLİR: 10 makalenin düz metin hâli, build_insights.py yazar
vercel.json                   justdukkan.vercel.app → apex 308 (host eşleşmeli; preview deploy'lar etkilenmez)
assets/wordmark.png           ".justdukkan" logosu — beyaz harfler + alfa; CSS `mask` + currentColor ile tema rengini alır
assets/favicon.svg/-32.png/-512.png, apple-touch-icon.png   ".j" glifi (wordmark'tan kırpıldı), koyu yuvarlak kare
brand/linkedin-cover.png (2256×382), linkedin-cover-1x.png  LinkedIn kapak: koyu zemin, sağda ".j"
llms.txt                      LLM crawler'ları için şirket/hizmet/makale/iletişim özeti (markdown)
robots.txt                    Herkese Allow; AI crawler'lar (GPTBot, ClaudeBot, PerplexityBot, Google-Extended…) açıkça Allow; Sitemap satırı
sitemap.xml                   /, /tr/ (hreflang), /insights/ + 10 makale, /privacy/ + /tr/gizlilik/ (hreflang)
9ab21623bd51863e0413867377354055.txt   IndexNow anahtar dosyası (§8)
README.md                     Kısa repo açıklaması
tasks/todo.md                 İş listesi (geçmiş fazlar işaretli)
```

## 5. Sayfa yapısı (ana sayfa, EN/TR aynı sıra)

1. **Header** (sticky 52px): wordmark · Services · Expertise · Approach · Insights · **About** · Contact · **tema toggle** · EN/TR · **"Get in touch →"** (mailto). Nav ≤960px gizlenir; ≤400px'te dil seçici de gizlenir (footer'da kalır).
2. **Hero**: "We build the AI agent teams your company runs on." + alt metin (son cümle: hazır agent aboneliği değil) + "Get in touch" (mailto) + "What we do" (`#services`)
3. **Models bandı**: Claude, ChatGPT, Gemini, Kimi, DeepSeek, Mistral, Llama, Qwen, Grok — monokrom inline SVG (lobehub `@lobehub/icons-static-svg`), tek satır
4. **Services** (4 kart, `grid grid-4`): Agent Team Design · Build & Deployment · Integrations: API & MCP · Operate & Maintain
5. **Expertise** (8 madde, 2 sütun): hub-and-spoke, MCP & tool design, agent skills & instructions, knowledge/retrieval, evals & guardrails, cloud (AWS/GCP), API & system integration, cost & operations
6. **Reference pattern → interaktif demo** (`#demo`, `assets/demo.js`): mock "JustDukkan Orchestrator" konsolu. Sol: 3 çalıştırma (Invoice intake / Support triage / Vendor onboarding). Orta: animasyonlu log (orchestrator → agent → tool çağrısı → **Human review: Approve/Reject** → done). Sağ: spoke'lar (aktif olan yeşil), tool sayacı, Replay. Sabit yükseklik 460px, log içeride kayar. Görünür olunca otomatik başlar (scroll-rect kontrolü; IntersectionObserver arka plan sekmesinde çalışmadığı için kullanılmadı). EN/TR string'ler `document.documentElement.lang`'a göre.
7. **Outcomes** (3): generic tools → sürece göre şekillenen sistem · manual hours → takımın uçtan uca yürüttüğü iş · eskiyen proje → bakımda tutulan sistem
8. **Approach** (4 adım, hizmetlerle hizalı): 01 · Discover → 02 · Design → 03 · Build → 04 · Operate
9. **FAQ** (8 soru, `<details>` akordeon, ilki açık; FAQPage schema). **Metinler her sayfada iki yerde**: JSON-LD `mainEntity` + görünür `<details>`; EN/TR dört kopya senkron kalmalı.
10. **Contact** (`#contact`): başlık + açıklama → **"Get in touch" butonu** (mailto) + "Tell us about the process in a few lines and we will get back to you as soon as possible." → ayraç **"or book a call"** → **Cal.com inline embed** (`#cal-inline`)
11. **Footer**: wordmark + EN/TR; sütunlar Company (About + Open source work linkleri, yasal ad, adres, EIN) / Contact (e-posta, tel, WhatsApp) / Insights (ilk 4 makale + "All insights"); "© 2026 JustDukkan, LLC"

**Insights** (`/insights/`, EN): liste + **10 makale**, `tools/articles.py`'daki sırayla: designing-the-agent-team, hub-and-spoke-agent-architecture, agent-topologies, mcp-server-and-tool-design, connecting-agents-to-your-apis, agent-skills, delegate-to-human, human-in-the-loop-for-agentic-systems, operating-agentic-systems, process-automation-architecture. Sıra = anlatı sırası; footer ilk 4'ü gösterir. Her makale: breadcrumb, hero, prose (720px), makale sonu FAQ, CTA kutusu ("Get in touch" mailto + "Book a call" `/#contact`). TR makale yok; TR sayfasındaki Insights linki EN'e gider.

Bölüm başlıklarının üstünde küçük "eyebrow" etiket **yok** (kaldırıldı; sadece models bandında bir etiket var). Metinlerde uzun çizgi (—) **kullanılmıyor**.

## 6. Tasarım sistemi

- Referans: **cursor.com**'un yapısal dili (renk, tipografi, container'lar); içerik değil.
- Tokenlar (`:root`): bg `#f7f7f4` · fg `#26251e` · card `#f0efeb` · card-hover `#ebeae5` · accent `#34785c`. Dark: bg `#14120b` · fg `#edecec` · card `#1b1913` · hover `#201e18` · accent `#4fa37e`.
- **Tema**: varsayılan sistem tercihi. Toggle `data-theme="light|dark"` yazar, `localStorage["jd-theme"]`'de saklar. Head'deki inline `jdTheme` script'i (`current()`, `toggle()`) flash'ı önler. **Dark tokenlar CSS'te iki yerde**: `@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) }` ve `:root[data-theme="dark"]` — token eklerken ikisini de güncelle. Toggle ikonu da aynı iki seçiciyle değişir.
- **Tek font: Inter** (Google Fonts, 400/500/600). Başlıklar Inter 400, `letter-spacing -0.03em`. Serif/JetBrains Mono YOK; kod için sistem mono.
- Container akışkan: `padding: 0 clamp(24px, 12vw, 260px)`, `max-width 1400px`. Prose 680–720px. Demo, takvim, FAQ ~820–1040px.
- Butonlar: primary (fg zemin, bg yazı, hover accent) + ghost (1px border). Kartlar 1px border, radius 12px, gölge yok.
- Logo: yalnızca wordmark; ekstra işaret/ikon ekleme.
- Cal.com: inline embed (`Cal.ns.consultation("inline", …)`), tema `jdTheme.current()`; toggle'da embed **yeniden oluşturulur** (Cal'ın `ui` tema güncellemesi inline'da işlemiyor). Renkler `cssVarsPerTheme` ile site paletine eşlenmiş. Alt "Cal.com" yazısı iframe'in alt 90px'i kırpılarak gizleniyor (`.cal-inline iframe { margin-bottom:-90px; clip-path: inset(0 0 90px 0) }`; `clip-path` şart, çünkü form adımında iframe 530px'e düşüyor ve `.cal-inline`'ın `min-height:560px`'i yalnız negatif margin ile kırpmayı boşa çıkarıyordu); `hideEventTypeDetails:false` (sol panelde "JustDukkan · Solution Consultation" görünür).
- Responsive: ≤900px grid'ler 2 sütun, demo sağ panel gizli; ≤640px tek sütun, nav linkleri gizli, demo yüksekliği auto. Yatay taşma olmamalı.

## 7. Cache-bust kuralı (ÖNEMLİ)

Cloudflare `styles.css`, `demo.js` ve `consent.js`'i cache'ler. Bunlar değişince **`?v=N`'i artır**: `index.html`, `tr/index.html`, `tools/build_insights.py` (sonra build), **`privacy/index.html`, `tr/gizlilik/index.html`**. Şu an **styles.css?v=20**, **demo.js?v=9**, **consent.js?v=1**. Artırmazsan canlıda eski CSS + yeni HTML görünür ("site bozuldu" olayının sebebi buydu). HTML cache'lenmez; canlı kontrolde yine de `?x=<rastgele>` ekle. Favicon linkleri `?v=2`.

## 8. SEO / GEO — yapılanlar

- **JSON-LD `@graph`** (ana sayfalar): `Organization`+`ProfessionalService` (yasal ad, adres, EIN=`taxID`, telefon, e-posta, diller, `knowsAbout`, **4 hizmetlik** `OfferCatalog`, `contactPoint`→Cal, `sameAs`: LinkedIn, GitHub org, Cal), `WebSite`, `WebPage`, `FAQPage`. Makalelerde `Article` + `BreadcrumbList` + `FAQPage`. Değişiklikte JSON geçerliliğini kontrol et.
- **OG/paylaşım**: her sayfada `og:image` (EN `og-cover.png`, TR `og-cover-tr.png`), boyut, alt ve `twitter:card=summary_large_image`. Değiştirmek için `brand/og-source.html` + §10'daki komut.
- **GA4**: Measurement ID **`G-C8T8T596HD`** (`consent.js` başında `GA_ID`; property `justdukkan.com`, time zone Türkiye, USD). Realtime'da doğrulandı (2026-09-13). Onay olmadan Google'a istek gitmez; canlı testte Chrome MCP'de `g/collect` 503 görünür (o tarayıcıda engelleyici), curl 204; GA'yı Enes'in tarayıcısından doğrula. Property Enes'in Google hesabında. Onay modeli §1.
- `llms.txt`, `robots.txt`, `sitemap.xml` (**15 URL**: /, /tr/, /insights/ + 10 makale, /privacy/, /tr/gizlilik/), `<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">`, canonical, hreflang en/tr/x-default, OG meta, theme-color.
- **Google Search Console**: domain property doğrulandı (DNS TXT), sitemap gönderildi (2026-09-13). İlk 4 Insights sayfası indekslendi; `/` beklemedeydi. 2026-09-22 pivotundan sonra ana sayfalar ve 6 yeni makale yeniden taranmayı bekliyor.
- **Bing Webmaster**: GSC'den import edildi (sitemap 48 saat sonra görünür dendi).
- **IndexNow**: anahtar `9ab21623bd51863e0413867377354055` (dosya repoda). Son gönderim 2026-09-22, 9 URL (pivot sonrası ana sayfalar + 6 yeni makale). Yeni/değişen sayfa için:
  `curl -X POST https://api.indexnow.org/indexnow -H 'Content-Type: application/json' -d '{"host":"justdukkan.com","key":"9ab21623bd51863e0413867377354055","keyLocation":"https://justdukkan.com/9ab21623bd51863e0413867377354055.txt","urlList":["https://justdukkan.com/…"]}'`
- **Dış varlıklar**: LinkedIn şirket sayfası (About metni = llms.txt özeti); GitHub org; **`github.com/justdukkan/invoice-intake-mcp`** (MIT, Python, mcp 2.x `MCPServer`; read/commit iki server, tipli hatalar, sunucu tarafı onay kilidi, audit log, orkestratör, pytest + evals; lokal `~/projects/invoice-intake-mcp`, venv Python 3.12) → PyPI `invoice-intake-mcp` 0.1.1 (`uvx invoice-intake-mcp --role read|commit`) → **MCP Registry `com.justdukkan/invoice-intake-mcp` v0.1.1 active** (DNS auth; özel anahtar `~/.config/mcp-registry/justdukkan-ed25519.pem`, repoya girmez). GitHub org namespace'i (`io.github.justdukkan`) çalışmadı (OAuth app org rolünü görmedi) — DNS yolu kullan.
- **awesome-mcp-servers PR #14311** açık (fork `justdukkan/awesome-mcp-servers`, branch `add-invoice-intake-mcp`, Finance & Fintech bölümü).
- Cal.com profili: bio metni eklendi, isim JustDukkan, avatar wordmark.

## 9. Açık işler

Kaynak: bu liste. `tasks/todo.md` tamamlanmış fazların kaydını tutar.

### 9.1 Enes'te (dashboard / hesap işleri, kod gerekmez)
- [ ] **GA4 → Data filters → Internal Traffic** filtresini *Testing*'den **Active**'e al (kural tanımlı: `176.88.102.0/24`). Aktif etmezsen kendi ziyaretlerin raporda kalır.
- [ ] **GA4 → Admin → Product links → Search Console** bağla (arama sorguları GA'da görünsün).
- [ ] **Search Console**: sitemap'i yeniden gönder (15 URL oldu); 1-2 hafta sonra pivot sonrası indeksleme kontrolü, gerekirse URL Inspection → Request indexing.
- [ ] **Bing Webmaster**: sitemap ve IndexNow sekmesi kontrolü; URL Submission ile yeni makaleler.
- [ ] **Vercel**: www → apex yönlendirmesi 307, istersen 308 yap (Domains → www → Edit → status code). Opsiyonel: Cloudflare'de apex'i DNS-only'ye almak cache-bust derdini bitirir.
- [ ] **LinkedIn kişisel profil**: JustDukkan deneyimi ekle (unvan pivota uygun: "Founder, JustDukkan · custom AI agent teams"); yeni makaleleri paylaş. Şirket sayfası About metnini `llms.txt` ilk paragrafıyla eşitle.
- [ ] **Schema doğrulama**: `validator.schema.org` ve Google Rich Results Test ile `/`, `/tr/`, `/about/`, `/work/`, `/insights/` ve bir makale sayfasını geçir.
- [ ] **invoice-intake-mcp README** son satırı hâlâ "AI solutions architecture" diyor (başka repo); pivota göre güncelle.
- [ ] **Dizinler**: Clutch.co, GoodFirms, Crunchbase profilleri (§2 bilgileri + llms.txt özeti; hizmet ağırlığı pivota göre: AI agent development / AI consulting / system integration).
- [ ] **awesome-mcp-servers PR #14311** merge takibi.

### 9.2 Kodda / sitede (Claude ile)
- [ ] **TR Insights altyapısı** (`/tr/insights/`) kurulacak mı, karar. Kurulursa `build_insights.py`'a TR modu + hreflang çiftleri + TR liste sayfası gerekir.
- [ ] Ayda 1-2 yeni makale. Aday konular: support triage mimarisi · agent takımı maliyet modeli · TR "şirketler için agentic sistemler 101" · retrieval hatları.
- [ ] Sertifikalar alındıkça siteye/LinkedIn'e rozet (Enes onayıyla; şu an sitede sertifika gösterilmiyor, §1).

### 9.3 En yüksek etkili iş
- [ ] **İlk gerçek işten vaka çalışması.** Uydurma metrik yazmama kuralı yüzünden sitede hâlâ tek bir sayı yok; ilk gerçek sonuç en güçlü sinyal olacak.

### 9.4 Düzenli kontrol
- [ ] Haftalık görünürlük testi: ChatGPT / Perplexity'de "custom AI agent team", "build AI agent team for company", "MCP server development consultant", "agentic system maintenance".

## 10. Rutin işlemler

- **Metin/HTML değişikliği**: `index.html` + `tr/index.html` **ikisini de** güncelle (FAQ metni değişiyorsa her sayfada JSON-LD + görünür blok, yani 4 kopya) → commit → push → 1 dk sonra `curl -sL "https://justdukkan.com/?x=$RANDOM" | grep …` ile doğrula.
- **CSS/JS değişikliği**: düzenle → `?v=N` artır (index, tr/index, build_insights, privacy ×2) → build_insights → commit/push.
- **Yeni makale**: `tools/articles.py`'a dict ekle (`date` alanı = yayın tarihi; sıra = index sırası) → `python3 tools/build_insights.py` → `sitemap.xml` + `llms.txt` makale listesi → footer ilk 4 makaleyi gösteriyor, değişirse `index.html`, `tr/index.html`, `privacy/index.html`, `tr/gizlilik/index.html` → IndexNow ping.
- **Hizmet/şirket bilgisi değişikliği**: HTML + JSON-LD + `llms.txt` + LinkedIn/dış profiller senkron.
- **invoice-intake-mcp yeni sürüm**: `pyproject.toml` + `server.json` version → `.venv/bin/python -m build` → Enes: `.venv/bin/twine upload dist/*` (`__token__` + PyPI token) → `mcp-publisher login dns --domain justdukkan.com --private-key "$(/opt/homebrew/opt/openssl@3/bin/openssl pkey -in ~/.config/mcp-registry/justdukkan-ed25519.pem -noout -text | grep -A3 priv: | tail -n +2 | tr -d ' :\n')" && mcp-publisher publish`.
- **OG görselini yeniden üret**: lokal sunucu açıkken
  `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu --hide-scrollbars --force-device-scale-factor=1 --window-size=1200,630 --virtual-time-budget=8000 --screenshot=assets/og-cover.png "http://127.0.0.1:8765/brand/og-source.html"` (TR için `?lang=tr`, çıktı `og-cover-tr.png`).
- **Lokal önizleme**: `python3 -m http.server 8765 --bind 127.0.0.1` (repo kökünde); Chrome MCP ile macmini tarayıcısı. Arka plan sekmesinde timer/IO throttling olur; demo testini görünür sekmede yap.
- **Terminal notu (Enes)**: Claude Code prompt'unda `! komut` çalıştırılır; zsh'de `!` yazma.

## 11. Bilinen tuhaflıklar

- Vercel CLI `vercel ls` çıktısı bazen boş görünür; deploy'u `https://justdukkan.com` içeriğinden doğrula.
- Cloudflare e-posta adreslerini `/cdn-cgi/l/email-protection` ile değiştirir; canlı HTML'de `enes@` aramak başarısız olabilir.
- Cal.com embed dar ekranda (<~768px) mobil düzene geçer (takvim tek sütun).
- **Header taşması düzeltildi** (2026-09-23, styles v21): nav ≤960px gizli, ≤1200px nav boşlukları dar, ≤560px container yan boşluğu 20px, ≤400px dil seçici gizli ve CTA küçük. 320-1440px arası tüm sayfa tiplerinde ölçülen taşma 0.
- `vercel.json`'da `source` **regex** olmalı (`/(.*)`); `"/:path*"` biçimi `/` ve `/insights/` gibi dizin URL'lerinde eşleşmiyordu.
- Search Console'da property "Domain" tipi olduğu için Bing import'unda "https://" boş görünmüştü; normal.
- Cal.com embed'i, Enes'in cal.com'a giriş yaptığı tarayıcıda formu hesap bilgileriyle (ad/e-posta) dolu ve hesap dilinde (TR) gösterir; ziyaretçi bunları görmez. Dil ziyaretçinin `Accept-Language`'ına göre gelir, embed'de dil zorlayan parametre yok (`lang/locale/hl/lng`, `NEXT_LOCALE` denendi, işlemiyor). Kontrol için gizli pencere kullan.
