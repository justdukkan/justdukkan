/* Interactive orchestrator demo — simulated runs, no backend. */
(function () {
  var lang = document.documentElement.lang === 'tr' ? 'tr' : 'en';

  var T = {
    en: {
      title: 'JustDukkan Orchestrator · Acme Ops',
      runs: 'Runs', spokes: 'Spokes', tools: 'Tool calls', replay: 'Replay',
      approve: 'Approve', reject: 'Reject', running: 'Running', done: 'Done', waiting: 'Waiting for approval',
      rejected: 'Returned to requester, nothing changed', request: 'Request',
      orchestrator: 'Orchestrator', human: 'Human review'
    },
    tr: {
      title: 'JustDukkan Orkestratör · Acme Ops',
      runs: 'Çalıştırmalar', spokes: 'Spoke\'lar', tools: 'Tool çağrısı', replay: 'Tekrar oynat',
      approve: 'Onayla', reject: 'Reddet', running: 'Çalışıyor', done: 'Tamamlandı', waiting: 'Onay bekliyor',
      rejected: 'Talep sahibine iade edildi, hiçbir şey değişmedi', request: 'Talep',
      orchestrator: 'Orkestratör', human: 'İnsan onayı'
    }
  }[lang];

  var RUNS = {
    en: [
      {
        id: 'invoices', name: 'Invoice intake', sub: 'Finance · 14 documents',
        request: 'Process the supplier invoices that arrived this morning and post the ones that match a purchase order.',
        spokes: ['Documents agent', 'Finance agent', 'ERP (MCP)', 'Human review'],
        steps: [
          { t: 'hub', text: 'Planned 4 steps · 2 agents · 3 tools' },
          { t: 'agent', who: 'Documents agent', text: 'Reading new files in inbox/invoices', spoke: 0 },
          { t: 'tool', call: 'drive.list_new(folder="inbox/invoices")', out: '14 files', spoke: 2 },
          { t: 'tool', call: 'ocr.extract("invoice_2291.pdf")', out: 'vendor=Norda Ltd · total=€7,420 · ref=PO-1187', spoke: 2 },
          { t: 'agent', who: 'Finance agent', text: 'Matching against open purchase orders', spoke: 1 },
          { t: 'tool', call: 'erp.match_po("PO-1187")', out: '3-way match OK · goods received 09-11', spoke: 2 },
          { t: 'human', text: 'Total above €5,000 — approval required before posting', spoke: 3 },
          { t: 'tool', call: 'erp.post_invoice(vendor="Norda Ltd", total=7420)', out: 'posted · INV-30412', spoke: 2 },
          { t: 'done', text: 'Done · 13 invoices remaining in queue · 41s · $0.06' }
        ]
      },
      {
        id: 'support', name: 'Support triage', sub: 'Support · overnight queue',
        request: 'Triage the overnight tickets, draft replies for the simple ones and escalate the rest.',
        spokes: ['Support agent', 'Knowledge base', 'Helpdesk (MCP)', 'Human review'],
        steps: [
          { t: 'hub', text: 'Planned 3 steps · 1 agent · 3 tools' },
          { t: 'agent', who: 'Support agent', text: 'Fetching new tickets', spoke: 0 },
          { t: 'tool', call: 'helpdesk.fetch(status="new", since="22:00")', out: '27 tickets', spoke: 2 },
          { t: 'tool', call: 'kb.search(query=<ticket summary>) ×27', out: '19 with a matching article · 8 without', spoke: 1 },
          { t: 'agent', who: 'Support agent', text: 'Drafted 19 replies from matching articles · 8 escalated to the team', spoke: 0 },
          { t: 'human', text: 'Send the 19 drafted replies?', spoke: 3 },
          { t: 'tool', call: 'helpdesk.reply(batch=19)', out: 'sent · 19 tickets set to "awaiting customer"', spoke: 2 },
          { t: 'done', text: 'Done · 8 tickets waiting for the team · 2m 10s · $0.31' }
        ]
      },
      {
        id: 'vendor', name: 'Vendor onboarding', sub: 'Procurement · Norda Ltd',
        request: 'Onboard Norda Ltd as a new supplier with net-30 terms.',
        spokes: ['Compliance agent', 'Finance agent', 'Registry / ERP (MCP)', 'Human review'],
        steps: [
          { t: 'hub', text: 'Planned 4 steps · 2 agents · 4 tools' },
          { t: 'agent', who: 'Compliance agent', text: 'Verifying company and screening', spoke: 0 },
          { t: 'tool', call: 'registry.lookup("Norda Ltd")', out: 'VAT valid · registered 2011 · Rotterdam', spoke: 2 },
          { t: 'tool', call: 'sanctions.screen("Norda Ltd")', out: 'no hits', spoke: 2 },
          { t: 'agent', who: 'Finance agent', text: 'Preparing vendor record', spoke: 1 },
          { t: 'human', text: 'Create vendor record with net-30 terms?', spoke: 3 },
          { t: 'tool', call: 'erp.create_vendor(name="Norda Ltd", terms="net30")', out: 'created · V-2093', spoke: 2 },
          { t: 'tool', call: 'email.send(template="welcome_pack", to="ap@norda.example")', out: 'sent', spoke: 2 },
          { t: 'done', text: 'Done · 58s · $0.09' }
        ]
      }
    ],
    tr: [
      {
        id: 'invoices', name: 'Fatura girişi', sub: 'Finans · 14 doküman',
        request: 'Bu sabah gelen tedarikçi faturalarını işle; satınalma siparişiyle eşleşenleri kayda al.',
        spokes: ['Doküman ajanı', 'Finans ajanı', 'ERP (MCP)', 'İnsan onayı'],
        steps: [
          { t: 'hub', text: '4 adım planlandı · 2 ajan · 3 tool' },
          { t: 'agent', who: 'Doküman ajanı', text: 'inbox/invoices klasöründeki yeni dosyalar okunuyor', spoke: 0 },
          { t: 'tool', call: 'drive.list_new(folder="inbox/invoices")', out: '14 dosya', spoke: 2 },
          { t: 'tool', call: 'ocr.extract("invoice_2291.pdf")', out: 'tedarikçi=Norda Ltd · toplam=€7.420 · ref=PO-1187', spoke: 2 },
          { t: 'agent', who: 'Finans ajanı', text: 'Açık satınalma siparişleriyle eşleştiriliyor', spoke: 1 },
          { t: 'tool', call: 'erp.match_po("PO-1187")', out: '3 yönlü eşleşme OK · mal kabul 09-11', spoke: 2 },
          { t: 'human', text: 'Toplam €5.000 üzerinde — kayıt öncesi onay gerekli', spoke: 3 },
          { t: 'tool', call: 'erp.post_invoice(vendor="Norda Ltd", total=7420)', out: 'kaydedildi · INV-30412', spoke: 2 },
          { t: 'done', text: 'Tamamlandı · kuyrukta 13 fatura · 41 sn · $0,06' }
        ]
      },
      {
        id: 'support', name: 'Destek triyajı', sub: 'Destek · gece kuyruğu',
        request: 'Gece gelen ticket\'ları triyajla, basit olanlara yanıt taslağı hazırla, kalanını ekibe yönlendir.',
        spokes: ['Destek ajanı', 'Bilgi bankası', 'Helpdesk (MCP)', 'İnsan onayı'],
        steps: [
          { t: 'hub', text: '3 adım planlandı · 1 ajan · 3 tool' },
          { t: 'agent', who: 'Destek ajanı', text: 'Yeni ticket\'lar çekiliyor', spoke: 0 },
          { t: 'tool', call: 'helpdesk.fetch(status="new", since="22:00")', out: '27 ticket', spoke: 2 },
          { t: 'tool', call: 'kb.search(query=<ticket özeti>) ×27', out: '19 eşleşen makale · 8 eşleşme yok', spoke: 1 },
          { t: 'agent', who: 'Destek ajanı', text: '19 yanıt taslağı hazırlandı · 8 ticket ekibe yönlendirildi', spoke: 0 },
          { t: 'human', text: '19 taslak yanıt gönderilsin mi?', spoke: 3 },
          { t: 'tool', call: 'helpdesk.reply(batch=19)', out: 'gönderildi · 19 ticket "müşteri bekleniyor"', spoke: 2 },
          { t: 'done', text: 'Tamamlandı · 8 ticket ekibi bekliyor · 2 dk 10 sn · $0,31' }
        ]
      },
      {
        id: 'vendor', name: 'Tedarikçi kaydı', sub: 'Satınalma · Norda Ltd',
        request: 'Norda Ltd\'yi 30 gün vadeli yeni tedarikçi olarak sisteme al.',
        spokes: ['Uyum ajanı', 'Finans ajanı', 'Sicil / ERP (MCP)', 'İnsan onayı'],
        steps: [
          { t: 'hub', text: '4 adım planlandı · 2 ajan · 4 tool' },
          { t: 'agent', who: 'Uyum ajanı', text: 'Şirket doğrulanıyor ve taranıyor', spoke: 0 },
          { t: 'tool', call: 'registry.lookup("Norda Ltd")', out: 'VKN geçerli · kuruluş 2011 · Rotterdam', spoke: 2 },
          { t: 'tool', call: 'sanctions.screen("Norda Ltd")', out: 'eşleşme yok', spoke: 2 },
          { t: 'agent', who: 'Finans ajanı', text: 'Tedarikçi kaydı hazırlanıyor', spoke: 1 },
          { t: 'human', text: '30 gün vadeli tedarikçi kaydı oluşturulsun mu?', spoke: 3 },
          { t: 'tool', call: 'erp.create_vendor(name="Norda Ltd", terms="net30")', out: 'oluşturuldu · V-2093', spoke: 2 },
          { t: 'tool', call: 'email.send(template="welcome_pack", to="ap@norda.example")', out: 'gönderildi', spoke: 2 },
          { t: 'done', text: 'Tamamlandı · 58 sn · $0,09' }
        ]
      }
    ]
  }[lang];

  var root = document.getElementById('demo');
  if (!root) return;

  var state = { run: 0, timer: null, token: 0, toolCalls: 0 };

  function el(tag, cls, html) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (html != null) e.innerHTML = html;
    return e;
  }
  function esc(s) { return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }

  function build() {
    root.innerHTML = '';
    root.appendChild(el('div', 'demo-titlebar',
      '<span class="demo-dots"><i></i><i></i><i></i></span><span class="demo-title">' + esc(T.title) + '</span>'));
    var body = el('div', 'demo-body');
    var side = el('aside', 'demo-side');
    side.appendChild(el('div', 'demo-h', esc(T.runs)));
    var list = el('ul', 'demo-runs');
    RUNS.forEach(function (r, i) {
      var li = el('li', 'demo-run' + (i === state.run ? ' is-active' : ''),
        '<span class="demo-status" data-run="' + i + '"></span><span><strong>' + esc(r.name) + '</strong><small>' + esc(r.sub) + '</small></span>');
      li.addEventListener('click', function () { select(i); });
      list.appendChild(li);
    });
    side.appendChild(list);
    var main = el('section', 'demo-main');
    var rail = el('aside', 'demo-rail');
    body.appendChild(side); body.appendChild(main); body.appendChild(rail);
    root.appendChild(body);
    root._main = main; root._rail = rail;
  }

  function setStatus(i, s) {
    var d = root.querySelector('.demo-status[data-run="' + i + '"]');
    if (d) d.className = 'demo-status ' + s;
  }

  function select(i) {
    state.run = i;
    root.querySelectorAll('.demo-run').forEach(function (li, k) { li.classList.toggle('is-active', k === i); });
    play();
  }

  function play() {
    clearTimeout(state.timer);
    var token = ++state.token;
    var run = RUNS[state.run];
    var main = root._main, rail = root._rail;
    state.toolCalls = 0;

    main.innerHTML = '';
    var head = el('div', 'demo-request');
    head.innerHTML = '<span class="demo-h">' + esc(T.request) + '</span><p>' + esc(run.request) + '</p>';
    main.appendChild(head);
    var tl = el('ol', 'demo-timeline');
    main.appendChild(tl);

    rail.innerHTML = '<div class="demo-h">' + esc(T.spokes) + '</div>';
    var spokes = el('ul', 'demo-spokes');
    spokes.appendChild(el('li', 'demo-spoke is-hub', '<i></i>' + esc(T.orchestrator)));
    run.spokes.forEach(function (s) { spokes.appendChild(el('li', 'demo-spoke', '<i></i>' + esc(s))); });
    rail.appendChild(spokes);
    var meter = el('div', 'demo-meter', '<span class="demo-h">' + esc(T.tools) + '</span><strong>0</strong>');
    rail.appendChild(meter);
    var replay = el('button', 'demo-replay', esc(T.replay) + ' ↻');
    replay.type = 'button';
    replay.addEventListener('click', play);
    rail.appendChild(replay);

    setStatus(state.run, 'is-running');
    var items = spokes.querySelectorAll('.demo-spoke');

    function activate(idx) {
      items.forEach(function (li) { li.classList.remove('is-active'); });
      if (idx == null) items[0].classList.add('is-active');
      else { items[idx + 1].classList.add('is-active'); items[idx + 1].classList.add('is-used'); }
    }

    var i = 0;
    function next() {
      if (token !== state.token) return;
      if (i >= run.steps.length) return;
      var s = run.steps[i++];
      var li = el('li', 'demo-step demo-' + s.t);
      if (s.t === 'hub') {
        li.innerHTML = '<span class="demo-who">' + esc(T.orchestrator) + '</span><span>' + esc(s.text) + '</span>';
        activate(null);
      } else if (s.t === 'agent') {
        li.innerHTML = '<span class="demo-who">' + esc(s.who) + '</span><span>' + esc(s.text) + '</span>';
        activate(s.spoke);
      } else if (s.t === 'tool') {
        li.innerHTML = '<code>' + esc(s.call) + '</code><span class="demo-out">→ …</span>';
        activate(s.spoke);
        state.toolCalls++;
        meter.querySelector('strong').textContent = state.toolCalls;
        setTimeout(function () {
          if (token !== state.token) return;
          li.querySelector('.demo-out').textContent = '→ ' + s.out;
          li.classList.add('is-done');
        }, 650);
      } else if (s.t === 'human') {
        li.innerHTML = '<span class="demo-who">' + esc(T.human) + '</span><span>' + esc(s.text) + '</span>' +
          '<span class="demo-actions"><button type="button" class="demo-btn demo-yes">' + esc(T.approve) + '</button>' +
          '<button type="button" class="demo-btn demo-no">' + esc(T.reject) + '</button></span>';
        activate(s.spoke);
        setStatus(state.run, 'is-waiting');
        li.querySelector('.demo-yes').addEventListener('click', function () {
          if (token !== state.token) return;
          li.classList.add('is-approved');
          li.querySelector('.demo-actions').innerHTML = '<span class="demo-decided">✓ ' + esc(T.approve) + '</span>';
          setStatus(state.run, 'is-running');
          state.timer = setTimeout(next, 500);
        });
        li.querySelector('.demo-no').addEventListener('click', function () {
          if (token !== state.token) return;
          li.classList.add('is-rejected');
          li.querySelector('.demo-actions').innerHTML = '<span class="demo-decided">✕ ' + esc(T.reject) + '</span>';
          var end = el('li', 'demo-step demo-done is-rejected', '<span class="demo-who">' + esc(T.orchestrator) + '</span><span>' + esc(T.rejected) + '</span>');
          tl.appendChild(end);
          activate(null);
          setStatus(state.run, 'is-done');
          i = run.steps.length;
        });
        tl.appendChild(li);
        tl.scrollTop = tl.scrollHeight;
        return; // wait for a click
      } else if (s.t === 'done') {
        li.innerHTML = '<span class="demo-who">' + esc(T.orchestrator) + '</span><span>' + esc(s.text) + '</span>';
        activate(null);
        setStatus(state.run, 'is-done');
      }
      tl.appendChild(li);
      tl.scrollTop = tl.scrollHeight;
      state.timer = setTimeout(next, s.t === 'tool' ? 1100 : 800);
    }
    state.timer = setTimeout(next, 300);
  }

  build();
  var started = false;
  function check() {
    if (started) return;
    var r = root.getBoundingClientRect();
    if (r.top < window.innerHeight * 0.85 && r.bottom > 0) {
      started = true;
      window.removeEventListener('scroll', check);
      play();
    }
  }
  window.addEventListener('scroll', check, { passive: true });
  check();
})();
